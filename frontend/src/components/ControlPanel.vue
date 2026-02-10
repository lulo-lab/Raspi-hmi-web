<template>
  <div>

    <h2>Steuerung</h2>

    <el-button
      type="primary"
      @click="loadState"
      style="margin-bottom: 20px"
    >
      Aktualisieren
    </el-button>


    <!-- NUMERISCH -->
    <el-card class="box-card">

      <template #header>
        Numerische Signale
      </template>

      <el-table
        :data="numerisch"
        border
        style="width: 100%"
      >

        <!-- Name -->
        <el-table-column
          prop="name"
          label="Name"
          width="auto"
        />

        <!-- Vorgabe -->
        <el-table-column
          label="Vorgabe"
          width="140"
        >
          <template #default="scope">
            <el-input-number
              v-model="scope.row.vorgabe"
              @change="setNumerisch(scope.row)"
              style="width: 120px"
            />
          </template>
        </el-table-column>

        <!-- Istwert -->
        <el-table-column
          prop="istwert"
          label="Istwert"
          width="120"
        />

        <!-- Einheit -->
        <el-table-column
          prop="einheit"
          label="Einheit"
          width="100"
        />

      </el-table>

    </el-card>


    <!-- BINAER -->
    <el-card class="box-card">

      <template #header>
        Binäre Signale
      </template>

      <el-table
        :data="binaer"
        border
        style="width: 100%"
      >

        <!-- Name -->
        <el-table-column
          prop="name"
          label="Name"
          width="auto"
        />

        <!-- Vorgabe -->
        <el-table-column
          label="Vorgabe"
          width="120"
        >
          <template #default="scope">
            <el-switch
              v-model="scope.row.vorgabe"
              @change="setBinaer(scope.row)"
            />
          </template>
        </el-table-column>

        <!-- Istwert -->
        <el-table-column
          label="Istwert"
          width="120"
        >
          <template #default="scope">
            <el-switch
              :model-value="scope.row.istwert"
              disabled
            />
          </template>
        </el-table-column>

      </el-table>

    </el-card>

  </div>
</template>


<script setup>

import { ref, onMounted } from "vue"

const API = "http://localhost:8000"

const numerisch = ref([])
const binaer = ref([])


// ------------------------------------------------
// STATE LADEN
// ------------------------------------------------

async function loadState() {

  try {

    const res = await fetch(`${API}/state`)
    const data = await res.json()


    numerisch.value = Object.entries(data.numerisch).map(
      ([name, value]) => ({
        name,
        vorgabe: value,
        istwert: value,
        einheit: ""
      })
    )


    binaer.value = Object.entries(data.binaer).map(
      ([name, value]) => ({
        name,
        vorgabe: value,
        istwert: value
      })
    )

  }
  catch (err) {

    console.error("State laden fehlgeschlagen:", err)

  }

}


// ------------------------------------------------
// NUMERISCH SETZEN
// ------------------------------------------------

async function setNumerisch(row) {

  try {

    await fetch(`${API}/numerisch/${row.name}`, {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        value: row.vorgabe
      })

    })

    row.istwert = row.vorgabe

  }
  catch (err) {

    console.error("Numerisch schreiben fehlgeschlagen:", err)

  }

}


// ------------------------------------------------
// BINAER SETZEN
// ------------------------------------------------

async function setBinaer(row) {

  try {

    await fetch(`${API}/binaer/${row.name}`, {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        value: row.vorgabe
      })

    })

    row.istwert = row.vorgabe

  }
  catch (err) {

    console.error("Binär schreiben fehlgeschlagen:", err)

  }

}


// ------------------------------------------------
// INIT
// ------------------------------------------------

onMounted(loadState)

</script>


<style scoped>

.box-card {
  margin-bottom: 20px;
}

</style>
