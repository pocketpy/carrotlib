mkdir -p build/ios
cd build/ios

FLAGS="-DCMAKE_TOOLCHAIN_FILE=3rd/pocketpy/3rd/ios.toolchain.cmake -DDEPLOYMENT_TARGET=13.0"

cmake -B os64 -G Xcode $FLAGS -DPLATFORM=OS64 ../..
cmake --build os64 --config Release

cmake -B simulatorarm64 -G Xcode $FLAGS -DPLATFORM=SIMULATORARM64 ../..
cmake --build simulatorarm64 --config Release

function merge() {
    echo "merge $1 $2"
    rm -f $1/libGame-$1.a
    find $1/** -name '*.a' -print
    libtool -static -o $1/libGame-$1.a $(find $1/** -name '*.a')
}

merge os64 Release-iphoneos
merge simulatorarm64 Release-iphonesimulator

rm -rf Game.xcframework

xcodebuild -create-xcframework \
    -library os64/libGame-os64.a \
    -library simulatorarm64/libGame-simulatorarm64.a \
    -output Game.xcframework
