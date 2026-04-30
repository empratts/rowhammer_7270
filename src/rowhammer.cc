#include "rowhammer.h"
#include "configuration.h"
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <string>
#include <iomanip>

namespace dramsim3 {

    Rowhammer::Rowhammer(std::string config_in, std::string output_dir,
                         std::string trace_in, unsigned int flip_threshold_in,
                         double vuln_scalar_in, unsigned int seed,
                         unsigned int trr_rows_in, double trr_ratio_in, bool ecc_in)
    : config_(config_in, output_dir),
      trace_file_(trace_in),
      flip_threshold(flip_threshold_in),
      vuln_scalar(vuln_scalar_in),
      generator(std::random_device{}()),
      dist(0, 1),
      trr_rows(trr_rows_in),
      trr_ratio(trr_ratio_in),
      trr_count(0),
      targets(0),
      flips(0),
      last_refresh(0),
      ecc(ecc_in),
      ecc_correctable(0),
      ecc_detectable_uncorrectable(0),
      ecc_undetectable(0)
    {
        if (seed)
        {
            generator.seed(seed);
        }
        refresh_interval = config_.tREFI * 8192; //7.6 microseconds * 8192 = 64 ms

    }
    
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

        // std::cout << "Rowhammer processing trace with flip threshold " << flip_threshold << ", vulnerability scalar " << vuln_scalar
        //           <<", trr_rows " << trr_rows << ", and trr_ratio " << trr_ratio << "\n";

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
        // Periodic Refresh
        if (clock_cycle - last_refresh > refresh_interval)
        {

            CountFlips();
            hits_.clear();
            last_refresh = clock_cycle;
        }
        // reading from a row refreshes it, so set its hit count to 0
        if(hits_.find(row) != hits_.end())
        {
            hits_[row] = 0;
        }

        if(hits_.find(row + 1) != hits_.end())
        {
            hits_[row + 1] += 1;
            if(trr_rows > 0)
            {
                TrackTRR(row + 1, clock_cycle);
            }
        }
        else
        {
            hits_[row + 1] = 1;
        }

        if(hits_.find(row - 1) != hits_.end())
        {
            hits_[row - 1] += 1;
            if(trr_rows > 0)
            {
                TrackTRR(row - 1, clock_cycle);
            }
        }
        else
        {
            hits_[row - 1] = 1;
        }


    }

    void Rowhammer::TrackTRR(unsigned int row, unsigned int clock_cycle)
    {
        if(trr_table_.find(row) != trr_table_.end())
        {
            trr_table_[row].hit_count += 1;
            trr_table_[row].last_updated = clock_cycle;
            
            if (trr_table_[row].hit_count > (flip_threshold * 2) * trr_ratio)
            {
                hits_[row] = 0;
                trr_count++;
                trr_table_.erase(row);
            }
        }
        else
        {
            //add and evict LRU
            trr_table_[row] = {.hit_count = 1, .last_updated = clock_cycle};
        }

        if (trr_table_.size() > trr_rows)
        {
            std::cout << "TRR: " << trr_count << " " << trr_table_.size() << "\n";
            unsigned int lru_row = row;
            unsigned int lru_cc = clock_cycle;
            for (auto i: trr_table_)
            {
                if (i.second.last_updated < lru_cc)
                {
                    lru_row = i.first;
                    lru_cc = i.second.last_updated;
                }
            }
            trr_table_.erase(lru_row);
        }
    }

    void Rowhammer::CountFlips()
    {
        if (!ecc)
        {
            double P_Flip = 0;
            unsigned int local_flips = 0;
            unsigned int local_targets = 0;
            for (auto i: hits_)
            {
                P_Flip = 1.0 - std::exp((double)(-1 * vuln_scalar * std::max(0, (int)(i.second - (flip_threshold * 2))))); //Factor of 2 accounts for double sided hammering

                if (P_Flip > .001)
                {
                    local_targets++;
                    if (dist(generator) < P_Flip)
                    {
                        local_flips++;
                    }
                }
            }
            flips += local_flips;
            targets += local_targets;
        }
        else
        {
            for (auto i: hits_)
            {
                // This computes the probability for a single bit to flip
                double P_individual_bit_flips = 1 - std::exp((double)(-1 * (vuln_scalar / 8192) * std::max(0, (int)(i.second - (flip_threshold * 2)))));
                // std::cout << "Chance of a single bit flipping: " << P_individual_bit_flips << "\n";
                // A row consists of 128 words
                for (int j = 0; j < 128; j++)
                {
                    // A word consists of 64 bits + 1 ecc bit
                    int flip_count_in_word = 0;
                    for (int k = 0; k < 65; k++)
                    {
                        if (dist(generator) < P_individual_bit_flips)
                        {
                            // std::cout << "Bit Flipped: \n";
                            flip_count_in_word++;
                        }
                    }

                    switch (flip_count_in_word) {
                        case 0:
                            break;
                        case 1:
                            ecc_correctable++;
                            break;
                        case 2:
                            ecc_detectable_uncorrectable++;
                            break;
                        default:
                            ecc_undetectable++;
                            break;
                    }
                }
            }

        }
    }

    void Rowhammer::PrintStats()
    {
        std::cout << "ECC_corr: \n" << ecc_correctable << "\n";
        std::cout << "ECC_det: \n" << ecc_detectable_uncorrectable << "\n";
        std::cout << "ECC_undet: \n" << ecc_undetectable << "\n";
        
    }
}