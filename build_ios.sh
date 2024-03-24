mkdir -p build/ios
cd build/ios

cmake -G Xcode -DCMAKE_TOOLCHAIN_FILE=~/ios-cmake/ios.toolchain.cmake -DPLATFORM=OS64COMBINED ../..
cmake --build . --config Release
