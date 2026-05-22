#ifndef INSTRUMENT_FM
#define INSTRUMENT_FM

#include <vector>
#include <string>
#include "instrument.h"
#include "envelope_adsr.h"

namespace upc {
  class InstrumentFM: public upc::Instrument {
    EnvelopeADSR adsr;
    float phase_c;   // fase del oscilador portador
    float phase_m;   // fase del oscilador modulador
    float step_c;    // incremento de fase del portador (por muestra)
    float step_m;    // incremento de fase del modulador (por muestra)
    float I;         // índice de modulación (lineal)
    float A;         // amplitud (velocity)
    int N1, N2;      // ratio c/m = N1/N2
  public:
    InstrumentFM(const std::string &param = "");
    void command(long cmd, long note, long velocity=1);
    const std::vector<float> & synthesize();
    bool is_active() const {return bActive;}
  };
}

#endif