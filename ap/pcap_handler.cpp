#include "pcap_handler.h"
#include "http.h"
#include "lib/radiotap-library/radiotap_iter.h"
#include "utils/Position.h"
#include <string>

using namespace std;
static Position *position = new Position();
string mac2string(unsigned char mac[6]) {
  char mac_c_str[18];
  sprintf(mac_c_str, "%02X:%02X:%02X:%02X:%02X:%02X\0", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
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


    /* Casting of the data from interface */
    auto user_data = ( pcap_handler_user_data *) user;

    auto rtap_hdr = ( struct ieee80211_radiotap_header *) bytes;

    if ( rtap_hdr->it_version == 0 ) {
        struct ieee80211_radiotap_iterator iter ;

        /**
         * @attention https://w1.fi/wpa_supplicant/devel/radiotap_8c.html
         */
        int error = ieee80211_radiotap_iterator_init(&iter, rtap_hdr, pkt->caplen, nullptr);
        if ( !error ) {
            auto wifi_hdr = ( struct ieee80211_header *) (bytes + iter._max_length);
            if ( (wifi_hdr->frame_control & 0x00c0) == 0x0080) {
                string source = "";
                struct timeval ts = pkt->ts; // get timestamp
                source = mac2string(wifi_hdr->address2); // get source adress
                RSSISample sample = {""};
                while(!error){
                                    error = ieee80211_radiotap_iterator_next (&iter );
                                    if(error){
                                        continue;
                                    }
                                    switch(iter.this_arg_index){
                                        case IEEE80211_RADIOTAP_DBM_ANTSIGNAL:
                                            if(sample.mac_address != ""){
                                                user_data->samples.push_back(sample);
                                            }
                                            sample = {source,((int) * (iter.this_arg) - 256 ),ts,-1};
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
                    /**
                     * set of the packets to send
                     */
                    RSSILog setToSend;

                    for (int i =0;i<user_data->samples.size();i++){

                        /**
                         * getiing the current timestamp
                         * @url https://man7.org/linux/man-pages/man2/gettimeofday.2.html
                         */
                        struct timeval cur{};
                        gettimeofday(&cur, nullptr);

                        int diff = ( cur.tv_sec - user_data->samples[i].ts.tv_sec );
                        if(diff >= 1){
                            cout << "Mac " << user_data->samples[i].mac_address
                                 << " Rssi " << user_data->samples[i].rssi
                                 << " Antenna "<< user_data->samples[i].antenna
                                 << endl;
                            printf("il y a %d seconds\n",diff);
                            setToSend.push_back(user_data->samples[i]);
                            user_data->samples.erase(user_data->samples.begin()+i);
                            i--;
                        }

                    }


                                if(!setToSend.empty())
                                    send_samples(setToSend, user_data->ap_mac_addr);



}
