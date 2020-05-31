//
// Created by abou on 31/05/2020.
//

#ifndef APNEW_UTIL_H
#define APNEW_UTIL_H
#include <pcap/pcap.h>

int pcap_findalldevs(pcap_if_t **alldevsp, char *errbuf);

void pcap_freealldevs(pcap_if_t *alldevs);
class Util {
private:
    char errbuf[PCAP_ERRBUF_SIZE];
    static Util *singleton;
public:


public:
    Util() {}
    static Util *getInstance();
    static void displayListInterface();

};





#endif //APNEW_UTIL_H
