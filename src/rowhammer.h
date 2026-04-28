#ifndef __ROWHAMMER_H
#define __ROWHAMMER_H

#include <fstream>
#include <iostream>
#include "configuration.h"
#include <random>
#include <map>


namespace dramsim3{

typedef struct trr_track_{
    unsigned int hit_count;
    unsigned int last_updated;
}TRR_Tracker;


    class Rowhammer{
        public:
            Rowhammer(std::string config_in, std::string output_dir,
                      std::string trace_in, unsigned int flip_threshold_in,
                      double vuln_scalar_in, unsigned int seed,
                      unsigned int trr_rows_in, double trr_ratio_in);
            ~Rowhammer();
            void ParseTrace();
            void HandleTransaction(unsigned int row, unsigned int clock_cycle);
            void CountFlips();
            void TrackTRR(unsigned int row, unsigned int clock_cycle);
            void PrintStats();
            unsigned int GetFlips() { return flips;}
            unsigned int GetTRRCount() { return trr_count;}

        protected:
            Config config_;
            std::ifstream trace_file_;
            unsigned int flip_threshold;
            double vuln_scalar;
            std::map<int, int> hits_;
            std::map<int, TRR_Tracker> trr_table_;
            std::mt19937 generator;
            std::uniform_real_distribution<double> dist;
            unsigned int trr_rows;
            double trr_ratio;
            unsigned int trr_count;
            unsigned int targets;
            unsigned int flips;
            unsigned int last_refresh;
            unsigned int refresh_interval;

    };
}

#endif