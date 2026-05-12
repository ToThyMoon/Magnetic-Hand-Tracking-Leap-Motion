int i = 0;
int address_pins[3] = {2,3,4};
const int num_receivers = 4;
const int num_rings = 6;
int magnetism_pins[num_receivers] = {A7,A2,A6,A3};
int magnet_value[4] = {0,0,0,0};
/*
Wrist - 1
Pinky - 2
Ring - 3

*/
int ring_numbers[num_rings] = {1, 2, 3, 4, 5, 6};

int magnet_values[num_rings][num_receivers];
char magnet_values_bytes[num_rings * num_receivers * 2];

unsigned long time_last_magnet = 0;
unsigned long duration_wait_magnet = 7000;
int current_ring = 0; 

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  
  for(int i = 0; i < 3; i++){
    pinMode(address_pins[i], OUTPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
  // analogReadResolution(12);
  // duration_per_reading = max(duration_per_reading, duration_wait_magnet * num_rings);
  set_address(ring_numbers[0]);
  // Serial.println("Done with setup Function!");
  // time_last_period = micros();
  time_last_magnet = micros();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
    String receivedString = Serial.readStringUntil('\n');
    
    for(i = 0; i < num_rings; i++){
      for(int j = 0; j < num_receivers; j++){
        Serial.print(magnet_values[i][j], DEC);
        Serial.print(" ");
      }
    }
    Serial.println();
  }

  if(micros() - time_last_magnet > duration_wait_magnet){
    time_last_magnet = micros();
    // Serial.println(current_ring);
    for(i = 0; i < num_receivers; i++){
      magnet_values[current_ring][i] = 0;
      for(int j = 0; j < 40; j++){
        magnet_values[current_ring][i] += analogRead(magnetism_pins[i]);
      }
      magnet_values[current_ring][i] = magnet_values[current_ring][i]/40;
      
      // magnet_values[current_ring][i] = analogRead(magnetism_pins[i]);
      // Serial.print(magnet_values[current_ring][i]);
      // Serial.print(" ");

      // magnet_values_bytes[(current_ring * num_receivers + i )*2] = 0
      // magnet_value[i] = analogRead(magnetism_pins[i]);
      // Serial.print(magnet_values[current_ring][i]);
      // Serial.print(",");
    }
    
    // Serial.println();

    current_ring++;   //comment out if only using one ring
    // set_address(ring_numbers[current_ring%num_rings]);
    if(current_ring >= num_rings){
      current_ring = 0;
    }

    set_address(ring_numbers[current_ring]);
  }
}

void set_address(int address){
  for(int i = 0; i < 3; i++){
    digitalWrite(address_pins[i], (address >> i) & 0x1);
  }
}
