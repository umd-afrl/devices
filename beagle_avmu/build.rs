extern crate bindgen;
extern crate fs_extra;

use std::env;
use std::path::PathBuf;
use fs_extra::file::{copy, CopyOptions};

fn main() {
    println!("{}", "cargo:rustc-link-search=/Users/julian/Documents/GitHub/devices/beagle_avmu/avmu");
    println!("cargo:rustc-link-lib=dylib=avmudll");

    let bindings = bindgen::Builder::default()
        // The input header we would like to generate
        // bindings for.
        .header("./avmu/libavmudll.h")
        // Finish the builder and generate the bindings.
        .generate()
        // Unwrap the Result and panic on failure.
        .expect("Unable to generate bindings");

    let out_path = PathBuf::from(env::var("OUT_DIR").unwrap());
    bindings
        .write_to_file(out_path.join("libavmu.rs"))
        .expect("Couldn't write bindings!");

    let res = copy("/Users/julian/Documents/GitHub/devices/beagle_avmu/avmu/libavmudll.dylib", "target/debug/libavmudll.dylib", &CopyOptions::new());
    match res {
        Ok(_v) => (),
        Err(e) => println!("Error copying dylib: {}", e),
    }
}