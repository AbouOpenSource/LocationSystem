//
// Created by abou on 30/05/2020.
//


#include <pcap.h>

int main(){
    pcap_if_t *alldevs, *d;
    pcap_t *fp;
    int i = 0;
    char errbuf[PCAP_ERRBUF_SIZE];
    u_int inum;

    if (pcap_findalldevs(&alldevs, errbuf) == -1)
    {
        fprintf(stderr,"Error in pcap_findalldevs: %s\n", errbuf);
        return 1;
    }

/* Print the list */
    for(d=alldevs; d; d=d->next)
    {
        printf("%d. %s", ++i, d->name);
        if (d->description)
            printf(" (%s)\n", d->description);
        else
            printf(" (No description available)\n");
    }

    if(i==0)
    {
        printf("\nNo interfaces found! Make sure WinPcap is installed.\n");
        return -1;
    }


}