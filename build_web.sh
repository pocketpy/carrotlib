mkdir -p build/web
cd build/web

emcmake cmake ../../CMakeLists.txt -DPLATFORM=Web -DCMAKE_BUILD_TYPE=Release
emmake make

# rm -rf CMakeFiles
# rm -rf CMakeCache.txt
# rm -rf Makefile
# rm -rf *.cmake
# rm -rf 3rd

mv Game.html index.html
