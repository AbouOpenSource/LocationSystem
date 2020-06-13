cmake_minimum_required(VERSION 3.15)
project(apNew)

set(CMAKE_CXX_STANDARD 14)

set(SOURCE_FILES pcap.cpp config/config.cpp config/config.h defines.h http.cpp http.h pcap_handler.cpp pcap_handler.h utils/Util.cpp utils/Util.h utils/Position.cpp utils/Position.h)
set(POCO_LIBRARY_STATIC -lPocoFoundation -lPocoNet)
set(RADIOTAP_LIBRARY_STATIC -lradiotap)
set(PCAP_LIBRARY_STATIC -lpcap)
if(UNIX AND NOT APPLE)
    set(LINUX TRUE)
endif()
if (LINUX)
    message("LINUX")
    add_executable(apNew ${SOURCE_FILES})
    target_link_libraries(apNew ${PCAP_LIBRARY_STATIC})
    target_link_libraries(apNew ${POCO_LIBRARY_STATIC})
    target_link_libraries(apNew ${RADIOTAP_LIBRARY_STATIC})
else ()
    message("NOT LINUX")


endif()

