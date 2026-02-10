
<template>
  <div>
    <h2>Registeransicht</h2>

    <el-button type="primary" @click="loadRegisters" style="margin-bottom: 20px;">
      Aktualisieren
    </el-button>

    <h3>Register</h3>
    <el-table :data="registerSoll" style="width: 100%" border>
      <el-table-column prop="index" label="Index" width="60"/>
      <el-table-column label="Inhalt">
        <template #default="scope">
          <el-input-number
            v-model="scope.row.value"
            :min="0"
            :max="65535"
            @change="updateRegister(scope.row)"
          />
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const API = "http://localhost:8000"

// Registerliste für die Tabelle
const registerSoll = ref([])


// ------------------------------------------------
// REGISTER LADEN
// ------------------------------------------------

async function loadRegisters() {
  try {

    const response = await fetch(`${API}/register`)

    if (!response.ok) {
      throw new Error(`HTTP Fehler: ${response.status}`)
    }

    const data = await response.json()

    // Backend liefert: { register: [int, int, int, ...] }

    registerSoll.value = data.register.map((value, index) => ({
      index: index,
      value: value
    }))

  } catch (err) {
    console.error("Fehler beim Laden der Register:", err)
  }
}


// ------------------------------------------------
// REGISTER SCHREIBEN
// ------------------------------------------------

async function updateRegister(row) {
  try {

    const response = await fetch(`${API}/register/${row.index}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        value: row.value
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP Fehler: ${response.status}`)
    }

  } catch (err) {
    console.error("Fehler beim Schreiben des Registers:", err)
  }
}


// ------------------------------------------------
// AUTOMATISCH LADEN BEI START
// ------------------------------------------------

onMounted(() => {
  loadRegisters()
})
</script>
