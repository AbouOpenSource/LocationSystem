//
// Created by abou on 31/05/2020.
//

#include "Util.h"
Util *Util::singleton = new Util;
Util *Util::getInstance() {
    if (!singleton)
        singleton = new Util;
    return singleton;
}

void Util::displayListInterface() {
    pcap_if_t *alldevsp,*temp;
    char *errbuf;
    int resultat= pcap_findalldevs(&alldevsp, errbuf);
    printf("\n the interfaces present on the system are:");
    int i =0;
    for(temp=alldevsp;temp;temp=temp->next)
    {
        printf("\n%d  :  %s",i++,temp->name);

    }
    printf("\n++++++++++++++++++++++++++++++++++++++++++++\n");
    pcap_freealldevs(alldevsp);
}
