// Define pinos dos botões e LED do relé
#define BUTTON_FOSFORO 23
#define BUTTON_POTASSIO 22
#define LED_RELE 2

// Bibliotecas utilizadas
#include "DHTesp.h"
#include <math.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Objeto do LCD I2C no endereço 0x27, com 16 colunas e 2 linhas
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Configuração do sensor DHT
const uint8_t DHT_PIN = 15;
const float GAMMA = 0.7f;
const float RL10 = 100.0f;
float LastValue_PH = 1.22f;
DHTesp dhtSensor;

// Últimos estados dos sensores/botões
uint8_t lastState_FOSFORO = HIGH;
uint8_t lastState_POTASSIO = HIGH;
const float desvio = 0.01f;

void setup() {
  Serial.begin(115200);
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);
  pinMode(BUTTON_FOSFORO, INPUT_PULLUP);
  pinMode(BUTTON_POTASSIO, INPUT_PULLUP);
  pinMode(LED_RELE, OUTPUT);

  lcd.init();            
  lcd.backlight();       
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Sistema iniciado");
  delay(1500);
  lcd.clear();
}

void loop() {
  uint8_t value_FOSFORO = digitalRead(BUTTON_FOSFORO);
  uint8_t value_POTASSIO = digitalRead(BUTTON_POTASSIO);

  float fosforo_mol_random = 0.0f;
  float potassio_mol_random = 0.0f;

  uint16_t analogValue = analogRead(35);  // 0–4095
  float voltage = analogValue / 1024.0f * 5.0f;
  float resistance = 2000.0f * voltage / fmax(1.0f - voltage / 5.0f, 0.01f);
  float value_PH = pow(RL10 * 1000.0f * pow(10.0f, GAMMA) / resistance, (1.0f / GAMMA));

  TempAndHumidity data = dhtSensor.getTempAndHumidity();
  float temperatura = data.temperature;
  float umidade = data.humidity;

  if (lastState_FOSFORO != value_FOSFORO) { 
    if (value_FOSFORO == LOW) {
      Serial.println();
      fosforo_mol_random = random(1, 10000 + 1) / 100.0f;
      Serial.print("Presença Fosforo: ");
      Serial.println(fosforo_mol_random);

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Fosforo:");
      lcd.setCursor(0, 1);
      lcd.print(fosforo_mol_random);
      delay(2000);
    }
  }

  if (lastState_POTASSIO != value_POTASSIO) {
    if (value_POTASSIO == LOW) {
      Serial.println();
      potassio_mol_random = random(1, 10000 + 1) / 100.0f;
      Serial.print("Presença Potassio: ");
      Serial.println(potassio_mol_random);

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Potassio:");
      lcd.setCursor(0, 1);
      lcd.print(potassio_mol_random);
      delay(2000);
    }
  }

  if (fabsf(LastValue_PH - value_PH) >= desvio) {
    Serial.println();
    Serial.print("Ph: ");
    Serial.println(value_PH);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("pH:");
    lcd.setCursor(0, 1);
    lcd.print(value_PH, 2);
    delay(2000);
  }

  if ((lastState_FOSFORO != value_FOSFORO && value_FOSFORO == LOW) || 
      (lastState_POTASSIO != value_POTASSIO && value_POTASSIO == LOW) || 
      fabsf(LastValue_PH - value_PH) >= desvio) {
    
    if (!isnan(temperatura) && !isnan(umidade)) {
      delay(500);
      Serial.println("Temp (°C): " + String(temperatura, 2));
      Serial.println("Humidity (%): " + String(umidade, 1));
      Serial.println();

      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Temp:");
      lcd.print(temperatura, 1);
      lcd.setCursor(0, 1);
      lcd.print("Umid:");
      lcd.print(umidade, 1);
      delay(2000);
    }
  }

  if (umidade >= 40.0f) {
    digitalWrite(LED_RELE, LOW);  // Bomba desligada
  } else {
    digitalWrite(LED_RELE, HIGH); // Bomba ligada
  }

  if ((lastState_FOSFORO != value_FOSFORO && value_FOSFORO == LOW) || 
      (lastState_POTASSIO != value_POTASSIO && value_POTASSIO == LOW) || 
      fabsf(LastValue_PH - value_PH) >= desvio) {

    if (!isnan(temperatura) && !isnan(umidade)) {
      Serial.println("============================================ COPIAVEL PARA SCRIPT PYTHON ============================================");
      Serial.println();
      Serial.print("log,");
      Serial.print(fosforo_mol_random); Serial.print(",");
      Serial.print(potassio_mol_random); Serial.print(",");
      Serial.print(value_PH, 2); Serial.print(",");
      Serial.print(temperatura, 2); Serial.print(",");
      Serial.println(umidade, 1);
      Serial.println();
      Serial.print("=====================================================================================================================");
      Serial.println();
    } 
  }

  lastState_FOSFORO = value_FOSFORO;
  lastState_POTASSIO = value_POTASSIO;
  LastValue_PH = value_PH;
}
