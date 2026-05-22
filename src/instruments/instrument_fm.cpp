#include <iostream>
#include <math.h>
#include "instrument_fm.h"
#include "keyvalue.h"

using namespace upc;
using namespace std;

InstrumentFM::InstrumentFM(const std::string &param)
  : adsr(SamplingRate, param) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(param);

  if (!kv.to_int("N1", N1)) N1 = 1;
  if (!kv.to_int("N2", N2)) N2 = 1;

  // I viene en semitonos, lo convertimos a índice lineal
  float I_semi;
  if (!kv.to_float("I", I_semi)) I_semi = 1.0F;
  I = pow(2.0F, I_semi / 12.0F) - 1.0F;

  phase_c = 0.0F;
  phase_m = 0.0F;
  step_c  = 0.0F;
  step_m  = 0.0F;
  A       = 1.0F;
}

void InstrumentFM::command(long cmd, long note, long vel) {
  if (cmd == 9) {  // key on
    bActive = true;
    adsr.start();
    A = vel / 127.0F;

    // frecuencia fundamental de la nota MIDI
    float f0 = 440.0F * pow(2.0F, (note - 69) / 12.0F);

    // frecuencia portadora y moduladora
    float fc = N1 * f0;
    float fm = N2 * f0;

    step_c = 2.0F * M_PI * fc / SamplingRate;
    step_m = 2.0F * M_PI * fm / SamplingRate;

    phase_c = 0.0F;
    phase_m = 0.0F;
  }
  else if (cmd == 8) {  // key off
    adsr.stop();
  }
  else if (cmd == 0) {  // extinción forzada
    adsr.end();
  }
}

const vector<float> & InstrumentFM::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i) {
    // oscilador modulador
    float mod = I * sin(phase_m);
    // oscilador portador modulado en frecuencia
    x[i] = A * sin(phase_c + mod);

    phase_m += step_m;
    if (phase_m >= 2.0F * M_PI) phase_m -= 2.0F * M_PI;

    // el portador avanza con su fase más la modulación
    phase_c += step_c;
    if (phase_c >= 2.0F * M_PI) phase_c -= 2.0F * M_PI;
  }

  adsr(x);
  return x;
}