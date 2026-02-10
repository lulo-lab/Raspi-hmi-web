<template>
  <div>
    <h2>Steuerung</h2>

    <el-button type="primary" @click="loadState" style="margin-bottom: 20px">
      Aktualisieren
    </el-button>

    <!-- Numerische Signale -->
    <el-card class="box-card" style="margin-bottom: 20px">
      <div slot="header">
        <span>Numerische Signale</span>
      </div>

      <el-table :data="numerischeSignals" style="width: 100%">
        <el-table-column prop="name" label="Signal" width="180"/>
        
        <el-table-column label="Sollwert">
          <template #default="scope">
            <el-input
              v-model.number="scope.row.soll"
              size="small"
              :disabled="scope.row.access !== 'rw'"
              @change="setNumSoll(scope.row)"
            >
              <template #append>{{ scope.row.unit }}</template>
            </el-input>
          </template>
        </el-table-column>

        <el-table-column label="Istwert">
          <template #default="scope">
            {{ scope.row.ist }} {{ scope.row.unit }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- Binäre Signale -->
    <el-card class="box-card">
      <div slot="header">
        <span>Binäre Signale</span>
      </div>

      <el-table :data="binaerSignals" style="width: 100%">
        <el-table-column prop="name" label="Signal" width="180"/>

        <el-table-column label="Sollwert">
          <template #default="scope">
            <el-switch
              v-model="scope.row.soll"
              :disabled="scope.row.access !== 'rw'"
              @change="setBinSoll(scope.row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="Istwert">
          <template #default="scope">
            <el-switch v-model="scope.row.ist" disabled />
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const numerischeSignals = reactive([])
const binaerSignals = reactive([])

const loadState = async () => {
  try {
    const res = await fetch('http://localhost:8000/state')
    const state = await res.json()

    // Numerische Signale
    numerischeSignals.length = 0
    Object.entries(state.numerisch.soll).forEach(([name, val]) => {
      numerischeSignals.push({
        name,
        soll: val.value,
        ist: state.numerisch.ist[name]?.value ?? 0,
        unit: val.unit ?? '',
        access: val.access ?? 'rw'
      })
    })

    // Binäre Signale
    binaerSignals.length = 0
    Object.entries(state.binaer.soll).forEach(([name, val]) => {
      binaerSignals.push({
        name,
        soll: val.value,
        ist: state.binaer.ist[name]?.value ?? false,
        access: val.access ?? 'rw'
      })
    })
  } catch (err) {
    console.error('Fehler beim Laden der Signale:', err)
  }
}

// Numerisch Sollwert setzen
const setNumSoll = async (row) => {
  try {
    await fetch(`http://localhost:8000/numerisch/soll/${row.name}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value: Number(row.soll) })
    })
  } catch (err) {
    console.error('Fehler beim Setzen des Sollwerts:', err)
  }
}

// Binär Sollwert setzen
const setBinSoll = async (row) => {
  try {
    await fetch(`http://localhost:8000/binaer/soll/${row.name}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ value: row.soll })
    })
  } catch (err) {
    console.error('Fehler beim Setzen des Sollwerts:', err)
  }
}

// Direkt beim Laden initialisieren
loadState()
</script>

<style scoped>
.box-card {
  margin-bottom: 20px;
}
</style>
