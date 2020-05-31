#include <fstream>
#include "http.h"
#include <Poco/URI.h>


bool doRequest(Poco::Net::HTTPClientSession& session, Poco::Net::HTTPRequest& request, Poco::Net::HTTPResponse& response)
{
    session.sendRequest(request);
    std::istream &rs = session.receiveResponse(response);
    std::cout << response.getStatus() << " " << response.getReason() << std::endl;
    return response.getStatus() != Poco::Net::HTTPResponse::HTTP_UNAUTHORIZED;

}




















void send_samples(RSSILog samples, std::string ap_mac_addr) {
  /*
   * TODO: Implement this function
   * It takes two parameters:
   * 	- samples with RSSI samples ordered by reception time
   * 	- ap_mac_addr the Raspberry Pi MAC address
   * 
   * It must send its MAC address as variable name ap
   * and a list of pairs DeviceMAC=RSSI where each DeviceMAC is unique
   * and RSSI are average RSSI values when multiple values exist for a
   * given DeviceMAC
   * 
   * The packet must be sent to http://localhost:8080/rssi
   * 
   * HTTP requests handling use Poco::Net API
   * */
  // TODO: your code here



    Poco::URI uri("http://localhost:5000/rssi");
    // prepare path
    std::string path(uri.getPathAndQuery());
    if (path.empty()) path = "/";

    std::string params = "?ap=" + ap_mac_addr;

    std::map<std::string, std::vector<int>> samplesMap;

    for (RSSISample sample: samples) {
        samplesMap[sample.mac_address].push_back(sample.rssi);
    }

    std::map<std::string, double> finalArray;

    for (auto const &val: samplesMap) {
        // val.first -> key
        // val.second -> value
        float sum = 0;
        float mean = 0;
        std::vector<int> actualVector = val.second;
        for (int i = 0; i < actualVector.size(); i++) {
            //sum += converToMW(actualVector[i]);
            sum += actualVector[i];

        }
        //mean = convertToDBm(sum / actualVector.size());
        mean = sum / actualVector.size();

        finalArray[val.first] = mean;
    }

    for (auto const &val: finalArray) {
        params += "&" + val.first + "=" + std::to_string(val.second);
    }

    path += params;
    //Poco::Net::HTTPClientSession session(uri.getHost(), uri.getPort());
    Poco::Net::HTTPRequest request(Poco::Net::HTTPRequest::HTTP_GET, path);
    //Poco::Net::HTTPResponse response;

   /* if (!doRequest(session, request, response)) {
        std::cout << "Failed to send anything." << std::endl;
    }
*/
}

