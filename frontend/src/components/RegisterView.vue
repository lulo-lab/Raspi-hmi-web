<template>
  <div>
    <h2>Registeransicht</h2>

    <el-button type="primary" @click="loadRegisters" style="margin-bottom: 20px;">
      Aktualisieren
    </el-button>

    <h3>SOLL-Register</h3>
    <el-table :data="registerSoll" style="width: 100%" border>
      <el-table-column prop="index" label="Index" width="80"/>
      <el-table-column label="Inhalt">
        <template #default="scope">
          <el-input-number
            v-model="scope.row.value"
            :min="0"
            :max="65535"
            @change="updateRegisterSoll(scope.row)"
          />
        </template>
      </el-table-column>
    </el-table>

    <h3 style="margin-top: 20px;">IST-Register (Simulation)</h3>
    <el-table :data="registerIst" style="width: 100%" border>
      <el-table-column prop="index" label="Index" width="80"/>
      <el-table-column label="Inhalt">
        <template #default="scope">
          <el-input-number
            v-model="scope.row.value"
            :min="0"
            :max="65535"
            @change="updateRegisterIst(scope.row)"
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const registerSoll = reactive([])
const registerIst = reactive([])

const loadRegisters = async () => {
  // SOLL
  const resSoll = await fetch('http://localhost:8000/register/soll')
  const dataSoll = await resSoll.json()
  registerSoll.length = 0
  dataSoll.forEach((val, idx) => registerSoll.push({ index: idx, value: val }))

  // IST
  const resIst = await fetch('http://localhost:8000/register/ist')
  const dataIst = await resIst.json()
  registerIst.length = 0
  dataIst.forEach((val, idx) => registerIst.push({ index: idx, value: val }))
}

const updateRegisterSoll = async (row) => {
  await fetch(`http://localhost:8000/register/soll`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values: registerSoll.map(r => r.value) })
  })
}

const updateRegisterIst = async (row) => {
  await fetch(`http://localhost:8000/register/ist`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ values: registerIst.map(r => r.value) })
  })
}

// direkt beim Laden initialisieren
loadRegisters()
</script>
