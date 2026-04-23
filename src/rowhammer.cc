#include "rowhammer.h"
#include "configuration.h"
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <string>

namespace dramsim3 {

    Rowhammer::Rowhammer(std::string config_in, std::string trace_in,
                         unsigned int flip_threshold_in, double vuln_scalar_in)
    : config_(config_in, "./"),
      trace_file_(trace_in),
      flip_threshold(flip_threshold_in),
      vuln_scalar(vuln_scalar_in),
      generator(std::random_device{}()), dist(0, 1) { }
    
    Rowhammer::~Rowhammer()
    {
        trace_file_.close();
    }

    void Rowhammer::ParseTrace()
    {
        unsigned int clock_cycle;
        std::string address_string, command;
        uint64_t address_int;
        Address address;

        std::cout << "Rowhammer processing trace with flip threshold " << flip_threshold << " and vulnerability scalar " << vuln_scalar << "\n";

        while(trace_file_ >> address_string >> command >> clock_cycle)
        {
            address_int = std::stoll(address_string,nullptr, 16);
            address = config_.AddressMapping(address_int);
            HandleTransaction(address.row, clock_cycle);
        }

        CountFlips();
    }

    void Rowhammer::HandleTransaction(unsigned int row, unsigned int clock_cycle)
    {
        // reading from a row refreshes it, so set its hit count to 0
        if(hits_.find(row) != hits_.end())
        {
            hits_[row] = 0;
        }

        if(hits_.find(row + 1) != hits_.end())
        {
            hits_[row + 1] += 1;
        }
        else
        {
            hits_[row + 1] = 1;
        }

        if(hits_.find(row - 1) != hits_.end())
        {
            hits_[row - 1] += 1;
        }
        else
        {
            hits_[row - 1] = 1;
        }

    }

    void Rowhammer::CountFlips()
    {
        std::cout << "Counting flips...\n";
        double P_Flip = 0;
        unsigned int flips = 0;
        for (auto i: hits_)
        {
            P_Flip = 1.0 - std::exp((double)(-1 * vuln_scalar * std::max(0, (int)(i.second - flip_threshold))));

            if (P_Flip > .000000001)
            {
                std::cout << "Row " << i.first << " has " << i.second << " hits and probability of flipping " << P_Flip;
                if (dist(generator) < P_Flip)
                {
                    flips++;
                    std::cout <<" and WAS FLIPPED.\n";
                }
                else
                {
                    std::cout <<" and was not flipped.\n";
                }
            }
        }
    }
}