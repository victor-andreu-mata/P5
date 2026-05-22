#include <iostream>
#include <math.h>
#include "seno.h"
#include "keyvalue.h"
#include <stdlib.h>
#include <fstream>

using namespace upc;
using namespace std;

InstrumentSeno::InstrumentSeno(const std::string &param) 
  : adsr(SamplingRate, param) {
  bActive = false;
  x.resize(BSIZE);

  KeyValue kv(param);
  int N;

  if (!kv.to_int("N", N))
    N = 40; // valor por defecto

  // Tabla con UN período completo de seno
  tbl.resize(N);
  float phase = 0, step = 2 * M_PI / (float) N;
  this->phase = 0;
  for (int i = 0; i < N; ++i) {
    tbl[i] = sin(phase);
    phase += step;
  }
}

void InstrumentSeno::command(long cmd, long note, long vel) {
  if (cmd == 9) {       // Tecla pulsada: comienza el ataque
    bActive = true;
    adsr.start();
    A = vel / 127.;
    this->step = 440 * pow(2, (note - 69) / 12.) * tbl.size() / SamplingRate;
  }
  else if (cmd == 8) {  // Tecla soltada: comienza el release
    adsr.stop();
  }
  else if (cmd == 0) {  // Sonido extinguido sin esperar release
    adsr.end();
  }
}

const vector<float> & InstrumentSeno::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i = 0; i < x.size(); ++i) {
    int idx = (int) phase;
    float frac = phase - idx;
    int idx_next = (idx + 1) % tbl.size();
    x[i] = A * (tbl[idx] * (1.0f - frac) + tbl[idx_next] * frac);
    phase += step;
    while (phase >= tbl.size())
      phase -= tbl.size();
  }

  // VOLCADO DE DATOS PARA LA GRÁFICA (solo primera llamada)
  static bool dumped = false;
  if (!dumped) {
    dumped = true;
    ofstream f("work/seno_data.csv");
    // Tabla
    f << "# TABLE\n";
    for (size_t i = 0; i < tbl.size(); ++i)
      f << i << "," << tbl[i] << "\n";
    // Señal generada
    f << "# SIGNAL\n";
    for (size_t i = 0; i < x.size(); ++i)
      f << i << "," << x[i] << "\n";
  }

  adsr(x);
  return x;
}