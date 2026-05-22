#include <iostream>
#include <math.h>
#include "instrument_dumb.h"
#include "keyvalue.h"

#include <stdlib.h>

using namespace upc;
using namespace std;

InstrumentDumb::InstrumentDumb(const std::string &param) 
  : adsr(SamplingRate, param) {
  bActive = false;
  x.resize(BSIZE);

  /*
    You can use the class keyvalue to parse "param" and configure your instrument.
    Take a Look at keyvalue.h    
  */
  KeyValue kv(param);
  int N;

  if (!kv.to_int("N",N))
    N = 40; //default value
  
  //Create a tbl with one period of a sinusoidal wave
  tbl.resize(N);
  float phase = 0, step = 2 * M_PI /(float) N;
<<<<<<< Updated upstream
  this->phase = 0;
=======
  tiss->phase = 0;
  this->step = 440*pow(2, (note-69)/12.) * step / SamplingRate;
  index = 0;
>>>>>>> Stashed changes
  for (int i=0; i < N ; ++i) {
    tbl[i] = sin(phase);
    phase += step;
  }
}


void InstrumentDumb::command(long cmd, long note, long vel) {
  if (cmd == 9) {		//'Key' pressed: attack begins
    bActive = true;
    adsr.start();

	  A = vel / 127.;
    this->step = 440*pow(2, (note-69)/12.) * tbl.size()/ SamplingRate;

    
	A = vel / 127.;



  }
  else if (cmd == 8) {	//'Key' released: sustain ends, release begins
    adsr.stop();
  }
  else if (cmd == 0) {	//Sound extinguished without waiting for release to end
    adsr.end();
  }
}


const vector<float> & InstrumentDumb::synthesize() {
  if (not adsr.active()) {
    x.assign(x.size(), 0);
    bActive = false;
    return x;
  }
  else if (not bActive)
    return x;

  for (unsigned int i=0; i<x.size(); ++i) {

    x[i] = A * tbl[(int) phase+0.5];
    phase += step;
    while(phase >= tbl.size()-0.5) {
      phase -= tbl.size();
    }
  }

    x[i] = A * tbl[(int) phase + o.5];
    phase+=step;
    while(pahase >=

  adsr(x); //apply envelope to x and update internal status of ADSR

  return x;
}
