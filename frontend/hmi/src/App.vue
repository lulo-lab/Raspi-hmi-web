<template>
  <div class="container">
    <h2>Numerische Sollwerte</h2>
    <div v-for="(item, index) in numericSollwerte" :key="index" class="row">
      <label class="label">{{ item.name }}</label>
      <input
        type="number"
        v-model.number="item.value"
        :min="item.min"
        :max="item.max"
        :step="getStep(item.value)"
        class="input"
      />
      <span class="unit">{{ item.unit }}</span>
    </div>

    <h2>Numerische Istwerte</h2>
    <div v-for="(item, index) in numericIstwerte" :key="index" class="row">
      <label class="label">{{ item.name }}</label>
      <input type="number" :value="item.value" disabled class="input" />
      <span class="unit">{{ item.unit }}</span>
    </div>

    <h2>Binäre Sollwerte</h2>
    <div v-for="(item, index) in binarySollwerte" :key="index" class="row">
      <label class="label">{{ item.name }}</label>
      <input type="checkbox" v-model="item.value" />
    </div>

    <h2>Binäre Istwerte</h2>
    <div v-for="(item, index) in binaryIstwerte" :key="index" class="row">
      <label class="label">{{ item.name }}</label>
      <span>{{ item.value ? 'Ein' : 'Aus' }}</span>
    </div>

    <button @click="syncValues">Synchronisieren</button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

// Hilfsfunktion Schrittweite
function getStep(value) {
  if (value >= 500) return 100
  if (value >= 50) return 10
  return 1
}

// Sollwerte
const numericSollwerte = reactive([
  { name: 'Spannung Soll', value: 24, min: 0, max: 60, unit: 'V' },
  { name: 'Strom Soll', value: 5, min: 0, max: 10, unit: 'A' },
  { name: 'Temperatur Soll', value: 20, min: -40, max: 125, unit: '°C' }
])

const numericIstwerte = reactive([
  { name: 'Spannung Ist', value: 0, unit: 'V' },
  { name: 'Strom Ist', value: 0, unit: 'A' },
  { name: 'Temperatur Ist', value: 0, unit: '°C' }
])

const binarySollwerte = reactive([
  { name: 'Enable', value: false },
  { name: 'Reset', value: false }
])

const binaryIstwerte = reactive([
  { name: 'Enable', value: false },
  { name: 'Reset', value: false }
])

// Hilfsfunktion Signalname extrahieren
function signalName(label) {
  return label.toLowerCase().split(' ')[0]
}

// Synchronisationsfunktion
async function syncValues() {
  // Numerische Sollwerte senden
  await Promise.all(
    numericSollwerte.map(item =>
      fetch(`http://localhost:8000/numerisch/soll/${signalName(item.name)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wert: item.value })
      })
    )
  )

  // Binäre Sollwerte senden
  await Promise.all(
    binarySollwerte.map(item =>
      fetch(`http://localhost:8000/binaer/soll/${signalName(item.name)}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ wert: item.value })
      })
    )
  )

  // Loopback auslösen
  await fetch('http://localhost:8000/loopback', { method: 'POST' })

  // Numerische Istwerte abrufen
  await Promise.all(
    numericIstwerte.map(async item => {
      const res = await fetch(`http://localhost:8000/numerisch/ist/${signalName(item.name)}`)
      const data = await res.json()
      item.value = data.wert
    })
  )

  // Binäre Istwerte abrufen
  await Promise.all(
    binaryIstwerte.map(async item => {
      const res = await fetch(`http://localhost:8000/binaer/soll/${signalName(item.name)}`)
      const data = await res.json()
      item.value = data.wert
    })
  )
}
</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 600px;
  font-family: Arial, sans-serif;
}

.row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.label {
  width: 150px;
}

.input {
  width: 100px;
  margin-right: 10px;
}

.unit {
  min-width: 20px;
}
</style>
