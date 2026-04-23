#ifndef __ROWHAMMER_H
#define __ROWHAMMER_H

#include <fstream>
#include <iostream>
#include "configuration.h"
#include <random>
#include <map>


namespace dramsim3{


    class Rowhammer{
        public:
            Rowhammer(std::string config_in, std::string trace_in, unsigned int flip_threshold_in, double vuln_scalar_in);
            ~Rowhammer();
            void ParseTrace();
            void HandleTransaction(unsigned int row, unsigned int clock_cycle);
            void CountFlips();

        protected:
            Config config_;
            std::ifstream trace_file_;
            unsigned int flip_threshold;
            double vuln_scalar;
            std::map<int, int> hits_;
            std::mt19937 generator;
            std::uniform_real_distribution<double> dist;

    };
}

#endif