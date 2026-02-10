<template>
  <div>
    <h2>Steuerung</h2>

    <el-button type="primary" @click="loadState" style="margin-bottom: 20px;">
      Aktualisieren
    </el-button>

    <!-- Numerische Signale -->
    <el-card class="box-card" style="margin-bottom: 20px;">
      <div slot="header">
        <span>Numerische Signale</span>
      </div>

      <el-table :data="numerischeSignals" style="width: 100%">
        <el-table-column prop="name" label="Signal" width="70" />

        <el-table-column label="Vorgabe" width="130">
          <template #default="scope">
            <el-input-number
              v-model.number="scope.row.vorgabe"
              :min="scope.row.min"
              :max="scope.row.max"
              size="small"
              :disabled="scope.row.access !== 'rw'"
              @change="setNum(scope.row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="Ist" width="70">
          <template #default="scope">
            {{ scope.row.istwert }}
          </template>
        </el-table-column>

        <el-table-column label="Einheit" width="30" prop="unit" />

        <el-table-column label="Access" width="30" prop="access" />

        <el-table-column label="Min" width="70" prop="min" />

        <el-table-column label="Max" width="70" prop="max" />
      </el-table>
    </el-card>

    <!-- Binäre Signale -->
    <el-card class="box-card">
      <div slot="header">
        <span>Binäre Signale</span>
      </div>

      <el-table :data="binaerSignals" style="width: 100%">
        <el-table-column prop="name" label="Signal" width="70" />

        <el-table-column label="Vorgabe" width="70">
          <template #default="scope">
            <el-switch
              v-model="scope.row.vorgabe"
              :disabled="scope.row.access !== 'rw'"
              @change="setBin(scope.row)"
            />
          </template>
        </el-table-column>

        <el-table-column label="Istwert" width="70">
          <template #default="scope">
            {{ scope.row.istwert }}
          </template>
        </el-table-column>

        <el-table-column label="Access" width="30" prop="access" />
      </el-table>
    </el-card>
  </div>
</template>


<script setup>
import { reactive } from "vue"

const numerischeSignals = reactive([])
const binaerSignals = reactive([])

const loadState = async () => {
  try {
    const res = await fetch("http://localhost:8000/state")
    const data = await res.json()

    numerischeSignals.length = 0
    binaerSignals.length = 0

    for (const [name, info] of Object.entries(data.numerisch)) {
      numerischeSignals.push({
        name,
        vorgabe: info.value,
        istwert: info.value,
        unit: info.unit || "",
        access: info.access || "rw",
        min: info.min ?? 0,
        max: info.max ?? 1000
      })
    }

    for (const [name, info] of Object.entries(data.binaer)) {
      binaerSignals.push({
        name,
        vorgabe: info.value,
        istwert: info.value,
        access: info.access || "rw"
      })
    }
  } catch (err) {
    console.error("Fehler beim Laden des States:", err)
  }
}

const setNum = async (row) => {
  try {
    const res = await fetch(`http://localhost:8000/numerisch/${row.name}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value: Number(row.vorgabe) })
    })
    const data = await res.json()
    row.istwert = data.value
  } catch (err) {
    console.error("Fehler beim Setzen des numerischen Werts:", err)
  }
}

const setBin = async (row) => {
  try {
    const res = await fetch(`http://localhost:8000/binaer/${row.name}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ value: Boolean(row.vorgabe) })
    })
    const data = await res.json()
    row.istwert = data.value
  } catch (err) {
    console.error("Fehler beim Setzen des binären Werts:", err)
  }
}

loadState()
</script>
