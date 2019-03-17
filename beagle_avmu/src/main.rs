#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

extern crate ws;
extern crate crossbeam;
#[macro_use]
extern crate serde;
extern crate serde_json;

use ws::{connect, listen, CloseCode, Handler, Message, Result, Handshake};
use std::thread;
use std::thread::sleep;
use crossbeam::channel::{Sender, Receiver, unbounded};
use std::time::Duration;

#[derive(Serialize, Deserialize, Debug)]
struct AvmuData {
    magnitude: Vec<i32>,
    peaks: Vec<i32>,
}


fn main() {
    let (avmu_sender, avmu_receiver): (Sender<AvmuData>, Receiver<AvmuData>) = unbounded();

    // Server WebSocket handler
    struct WSServer {
        rx: Receiver<AvmuData>,
        out: ws::Sender,
    }

    impl Handler for WSServer {
        fn on_open(&mut self, hs: Handshake) -> Result<()> {
            println!("Server got connection '{:?}'. ", hs.peer_addr);
            self.out.send(serde_json::to_string(&self.rx.recv().unwrap()).unwrap())
        }

        fn on_message(&mut self, msg: Message) -> Result<()> {
            println!("Server got message '{}'. ", msg);
            self.out.send(msg)
        }

        fn on_close(&mut self, code: CloseCode, reason: &str) {
            println!("WebSocket closing for ({:?}) {}", code, reason);
            println!("Shutting down server after first connection closes.");
            self.out.shutdown().unwrap();
        }
    }

    // Server thread
    let server = thread::spawn(move || listen("127.0.0.1:3012", |out| WSServer { rx: avmu_receiver.clone(), out }).unwrap());

    // Give the server a little time to get going
    sleep(Duration::from_millis(10));

    // Client thread
    let client = thread::spawn(move || {
        connect("ws://127.0.0.1:3012", |out| {
            out.send("Hello WebSocket").unwrap();

            move |msg| {
                println!("Client got message '{}'. ", msg);
                out.close(CloseCode::Normal)
            }
        }).unwrap()
    });

    avmu_sender.send(AvmuData { magnitude: vec![0], peaks: vec![] }).unwrap();

    let _ = server.join();
    let _ = client.join();

    println!("All done.")
}