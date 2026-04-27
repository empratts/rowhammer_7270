#include <iostream>
#include "./../ext/headers/args.hxx"
#include "cpu.h"
#include "rowhammer.h"

using namespace dramsim3;

int main(int argc, const char **argv) {
    args::ArgumentParser parser(
        "DRAM Simulator.",
        "Examples: \n."
        "./build/dramsim3main configs/DDR4_8Gb_x8_3200.ini -c 100 -t "
        "sample_trace.txt\n"
        "./build/dramsim3main configs/DDR4_8Gb_x8_3200.ini -s random -c 100");
    args::HelpFlag help(parser, "help", "Display the help menu", {'h', "help"});
    args::ValueFlag<uint64_t> num_cycles_arg(parser, "num_cycles",
                                             "Number of cycles to simulate",
                                             {'c', "cycles"}, 100000);
    args::ValueFlag<std::string> output_dir_arg(
        parser, "output_dir", "Output directory for stats files",
        {'o', "output-dir"}, ".");
    args::ValueFlag<std::string> stream_arg(
        parser, "stream_type", "address stream generator - (random), stream",
        {'s', "stream"}, "");
    args::ValueFlag<std::string> trace_file_arg(
        parser, "trace",
        "Trace file, setting this option will ignore -s option",
        {'t', "trace"});
    args::ValueFlag<int> threshold_arg(parser, "threshold_arg_int", 
                                                   "Bit Flip Threshold", 
                                                   {"threshold"}, 300000);
    args::ValueFlag<int> seed_arg(parser, "seed_arg_int", 
                                                   "RNG seed. 0 = Random (default)", 
                                                   {"seed"}, 0);
    args::ValueFlag<double> vuln_arg(parser, "vuln_arg_double", 
                                                   "Vulnerability scalar", 
                                                   {'v', "vuln"}, 0.0);
    args::ValueFlag<unsigned int> trr_rows_arg(parser, "trr_rows_int", 
                                                   "Number of rows to track for TRR. 0 = off.", 
                                                   {"trr"}, 0);
    args::ValueFlag<double> trr_ratio_arg(parser, "trr_ratio_double", 
                                                   "Ratio of the threshold to activate trr at. Requires trr_rows > 0. Default is 0.5", 
                                                   {"ratio"}, 0.5);
    args::Positional<std::string> config_arg(
        parser, "config", "The config file name (mandatory)");

    try {
        parser.ParseCLI(argc, argv);
    } catch (args::Help) {
        std::cout << parser;
        return 0;
    } catch (args::ParseError e) {
        std::cerr << e.what() << std::endl;
        std::cerr << parser;
        return 1;
    }

    std::string config_file = args::get(config_arg);
    if (config_file.empty()) {
        std::cerr << parser;
        return 1;
    }

    uint64_t cycles = args::get(num_cycles_arg);
    std::string output_dir = args::get(output_dir_arg);
    std::string trace_file = args::get(trace_file_arg);
    std::string stream_type = args::get(stream_arg);

    int bit_flip_threshold = args::get(threshold_arg);
    double vulnerability_scalar = args::get(vuln_arg);
    int seed = args::get(seed_arg);
    unsigned int trr_rows = args::get(trr_rows_arg);
    double trr_ratio = args::get(trr_ratio_arg);

    Rowhammer rh(config_file, output_dir, trace_file, bit_flip_threshold, vulnerability_scalar, seed, trr_rows, trr_ratio);

    rh.ParseTrace();

    CPU *cpu;
    if (!trace_file.empty()) {
        cpu = new TraceBasedCPU(config_file, output_dir, trace_file);
    } else {
        if (stream_type == "stream" || stream_type == "s") {
            cpu = new StreamCPU(config_file, output_dir);
        } else {
            cpu = new RandomCPU(config_file, output_dir);
        }
    }

    for (uint64_t clk = 0; clk < cycles || !cpu->Done(); clk++) {
        cpu->ClockTick();
    }
    cpu->PrintStats();

    rh.PrintStats();

    delete cpu;

    return 0;
}
