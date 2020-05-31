#ifndef _HTTP_H_
#define _HTTP_H_

#include "defines.h"

#include <Poco/Net/Net.h>
#include <Poco/Net/HTTPClientSession.h>
#include <Poco/Net/HTTPRequest.h>
#include <Poco/Net/HTTPResponse.h>
#include <Poco/Net/HTMLForm.h>

#include <map>
#include <set>
#include <cmath>
#include <iostream>





void send_samples(RSSILog samples, std::string ap_mac_addr);

#endif //_HTTP_H_
