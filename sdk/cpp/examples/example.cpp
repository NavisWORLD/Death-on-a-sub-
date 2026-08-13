#include <heartlight/hip.hpp>
#include <iostream>

int main() {
    heartlight::RhythmSignature rhythm;
    rhythm.algorithm = "heartlight-envelope-peaks-v1";
    rhythm.sample_rate = 44100;
    rhythm.duration_seconds = 5.0;
    std::cout << "HEARTLIGHT HIP " << heartlight::HIP_VERSION << "\n";
    std::cout << heartlight::DISCLOSURE << "\n";
    return 0;
}
