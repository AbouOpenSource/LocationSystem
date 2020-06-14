#include <cmath>
#include <fstream>
#include "http.h"
#include "utils/Position.h"
#include "config/config.h"
#include <Poco/URI.h>
#include<numeric>

float convertToDBm(float d);

bool doRequest(Poco::Net::HTTPClientSession& session, Poco::Net::HTTPRequest& request, Poco::Net::HTTPResponse& response)
{
    session.sendRequest(request);
    std::istream &rs = session.receiveResponse(response);
    std::cout << response.getStatus() << " " << response.getReason() << std::endl;
    return response.getStatus() != Poco::Net::HTTPResponse::HTTP_UNAUTHORIZED;

}

/**
 * @reauest form curl http://server_host:server_port/start_calibration?mac_addr=my_mac&x=my_x&y=my_y&z=my_z
 * @param samples
 * @param ap_mac_addr
 */
bool sendStartCalibration(Position *position, const std::string& ap_mac_addr) {
    Configuration *configuration = Configuration::getInstance();



    Poco::URI uri(configuration->getHttpPath()+"/start_calibration");
    std::string path(uri.getPathAndQuery());
    if (path.empty())
    {
        path = "/";
    }
    uri.addQueryParameter("mac_addr",ap_mac_addr);
    uri.addQueryParameter("x",std::to_string(position->getX()));
    uri.addQueryParameter("y",std::to_string(position->getY()));
    uri.addQueryParameter("z",std::to_string(position->getZ()));


    Poco::Net::HTTPClientSession session(uri.getHost(), uri.getPort());
    Poco::Net::HTTPRequest request(Poco::Net::HTTPRequest::HTTP_GET, path);
    Poco::Net::HTTPResponse response;

    if (!doRequest(session, request, response)) {

        std::cout << "Can not send the data : Error " << response.getStatus()<<std::endl;
        return false;
    }{
        return true;
    }

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

    Configuration *configuration = Configuration::getInstance();
    Poco::URI uri(configuration->getHttpPath()+"/rssi");
    std::string path(uri.getPathAndQuery());
    if (path.empty())
    {
        path = "/";
    }

    //uri.addQueryParameter("ap",ap_mac_addr);
    std::string params = "?ap=" + ap_mac_addr;

    std::map<std::string, std::vector<int>> mapMacRssiVector;

    for (const RSSISample& sample: samples) {
        mapMacRssiVector[sample.mac_address].push_back(sample.rssi);
    }

    std::map<std::string, double> arrayOfMean;

    for (auto const &item: mapMacRssiVector) {
        std::vector<int> vectorOf = item.second;
        arrayOfMean[item.first]={ std::accumulate(vectorOf.begin(), vectorOf.end(), 0.0)/vectorOf.size() };

    }
   // path += params;
    for(auto & item : arrayOfMean) {
        //uri.addQueryParameter(item.first,std::to_string(item.second));
        params += "&" + item.first + "=" + std::to_string(item.second);
    }
    path += params;
    std::cout << uri.getPath();
    std::cout<<"The query is :  "<<path<< ""<< std::endl;

    Poco::Net::HTTPClientSession session(uri.getHost(), uri.getPort());
    Poco::Net::HTTPRequest request(Poco::Net::HTTPRequest::HTTP_GET, path);
    Poco::Net::HTTPResponse response;

    if (!doRequest(session, request, response)) {
        std::cout << "Can not send the data : Error " << response.getStatus()<<std::endl;
    }

}

float convertToDBm(float val) {
    return std::log10(val) * 10;
}

float converToMW(int val) {
    return (float) pow(10.0, val / 10.0);
}
