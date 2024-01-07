rm -rf build/web
mkdir -p build/web
cp -r android/app/src/main/assets build/web
cd build/web
emcmake cmake ../../CMakeLists.txt -DPLATFORM=Web -DCMAKE_BUILD_TYPE=Release
emmake make
rm -rf CMakeFiles
rm -rf CMakeCache.txt
rm -rf Makefile
rm -rf cmake_install.cmake
rm -rf workdir

mv Game.html index.html
