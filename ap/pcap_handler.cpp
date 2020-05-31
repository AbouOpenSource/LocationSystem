#include "pcap_handler.h"
#include "http.h"
#include "lib/radiotap-library/radiotap_iter.h"
#include <string>

using namespace std;

string mac2string(unsigned char mac[6]) {
  char mac_c_str[18];
  sprintf(mac_c_str, "%02X:%02X:%02X:%02X:%02X:%02X\0", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  //    sprintf(mac_c_str, "%02X:%02X:%02X:%02X:%02X:%02X", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  return string{mac_c_str};
}

/*
 * \function process_pkts PCAP callback function
 * \param user a pointer (to be cast) to a RSSILog variable
 * \param pkt a pointer to a rtap header
 * \param bytes a pointer to the captured packet, starting by the radiotap header
 */
void process_pkts(u_char* user, const struct pcap_pkthdr *pkt, const u_char *bytes) {
  /*
   * TODO: for each packet, extract the source address, the RSSI value(s),
   * the antenna index when present, and get system time. Each RSSI goes
   * to one element in the user->samples vector.
   * After dealing with the packet, check the first vector element
   * timestamp against current time. If it is older than 1 second, send
   * the samples (call send_samples from http.h)
   * */

  // TODO: your code here


    auto user_data = ( pcap_handler_user_data *) user;

    auto rtap_hdr = ( struct ieee80211_radiotap_header *) bytes;

    if ( rtap_hdr->it_version == 0 ) {
        struct ieee80211_radiotap_iterator iter ;
        int err = ieee80211_radiotap_iterator_init(&iter, rtap_hdr, pkt->caplen, nullptr);
        if ( !err ) {
            auto wifi_hdr = ( struct ieee80211_header *) (bytes + iter._max_length);
            if ( (wifi_hdr->frame_control & 0x00c0) == 0x0080) {

                string source = "";
                struct timeval ts = pkt->ts; // get timestamp
                source = mac2string(wifi_hdr->address2); // get source adress
                RSSISample sample = {""};

                while(!err){
                    err = ieee80211_radiotap_iterator_next (&iter );
                    if(err){
                        continue;
                    }

                    switch(iter.this_arg_index){
                        case IEEE80211_RADIOTAP_DBM_ANTSIGNAL:
                            if(sample.mac_address != ""){
                                user_data->samples.push_back(sample);
                            }
                            sample = {
                                    source, //String mac adress
                                    ((int) * (iter.this_arg) - 256 ), //RSSI
                                    ts, //Timestamp
                                    -1 //Antenna
                            };
                            break;

                        case IEEE80211_RADIOTAP_ANTENNA:
                            sample.antenna = (int) * iter.this_arg;
                            break;
                    }
                }
                user_data->samples.push_back(sample);
            }
        }
    }

    RSSILog toSend;
    for (int i =0;i<user_data->samples.size();i++){

        struct timeval current;
        gettimeofday(&current, NULL);
        int diff = (current.tv_sec-user_data->samples[i].ts.tv_sec);
        if(diff >= 1){
            cout << "Send : Mac " << user_data->samples[i].mac_address << " Rssi " << user_data->samples[i].rssi << " Antenna " << user_data->samples[i].antenna << endl;
            printf("Emis il y a %d secondes\n",diff);
            toSend.push_back(user_data->samples[i]);
            user_data->samples.erase(user_data->samples.begin()+i);
            i--;
        }

    }
    if(toSend.size()>0){
        send_samples(toSend, user_data->ap_mac_addr);
    }
}
