<template>
  <div class="container">
    <h2>Numerische Sollwerte</h2>
    <div
      v-for="(item, index) in numericSollwerte"
      :key="index"
      class="row"
    >
      <label class="label">{{ item.name }}</label><el-input-number
    v-model="item.value"
    :step="getStep(item.value)"
    :min="item.min"
    :max="item.max"
    :controls="true"
    class="input"
  >
    <template #suffix>
      <span class="unit">{{ item.unit }}</span>
    </template>
  </el-input-number>
</div>

<h2>Numerische Istwerte</h2>
<div
  v-for="(item, index) in numericIstwerte"
  :key="index"
  class="row"
>
  <label class="label">{{ item.name }}</label>

  <el-input-number
    v-model="item.value"
    :controls="false"
    disabled
    class="input"
  >
    <template #suffix>
      <span class="unit">{{ item.unit }}</span>
    </template>
  </el-input-number>
</div>

<h2>Binäre Sollwerte</h2>
<div
  v-for="(item, index) in binarySollwerte"
  :key="index"
  class="row"
>
  <label class="label">{{ item.name }}</label>
  <el-switch v-model="item.value" />
</div>

<h2>Binäre Istwerte</h2>
<div
  v-for="(item, index) in binaryIstwerte"
  :key="index"
  class="row"
>
  <label class="label">{{ item.name }}</label>
  <el-tag
    :type="item.value ? 'success' : 'info'"
  >
    {{ item.value ? 'Ein' : 'Aus' }}
  </el-tag>
</div>

  </div>
</template><script setup>
import { reactive } from 'vue'

// Funktion zur dynamischen Schrittweite
function getStep(value) {
  if (value >= 500) return 100
  if (value >= 50) return 10
  return 1
}

// Beispiel-Daten numerische Sollwerte
const numericSollwerte = reactive([
  {
    name: 'Spannung Soll',
    value: 24,
    min: 0,
    max: 1000,
    unit: 'V'
  },
  {
    name: 'Strom Soll',
    value: 120,
    min: 0,
    max: 1000,
    unit: 'A'
  },
  {
    name: 'Leistung Soll',
    value: 600,
    min: 0,
    max: 5000,
    unit: 'W'
  }
])

// Beispiel-Daten numerische Istwerte
const numericIstwerte = reactive([
  {
    name: 'Spannung Ist',
    value: 23.7,
    unit: 'V'
  },
  {
    name: 'Strom Ist',
    value: 118.2,
    unit: 'A'
  },
  {
    name: 'Leistung Ist',
    value: 598,
    unit: 'W'
  }
])

// Beispiel-Daten binäre Sollwerte
const binarySollwerte = reactive([
  {
    name: 'Netzteil Enable',
    value: true
  },
  {
    name: 'Lüfter Enable',
    value: false
  }
])

// Beispiel-Daten binäre Istwerte
const binaryIstwerte = reactive([
  {
    name: 'Netzteil Status',
    value: true
  },
  {
    name: 'Fehler Status',
    value: false
  }
])
</script><style scoped>
.container {
  padding: 20px;
  max-width: 500px;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.label {
  width: 200px;
}

.input {
  width: 200px;
}

.unit {
  margin-left: 4px;
  color: #606266;
}

h2 {
  margin-top: 20px;
}
</style>
