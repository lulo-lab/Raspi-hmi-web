<template>

  <div style="padding:20px">

    <h1>FPGA HMI</h1>

    <el-button type="primary" @click="loadState">
      Aktualisieren
    </el-button>

    <br><br>

    <!-- NUMERISCHE SOLL -->
    <el-card>

      <template #header>
        Numerische Sollwerte
      </template>

      <div v-for="(value, name) in state.numerisch.soll" :key="name">

        <span style="width:150px; display:inline-block">
          {{ name }}
        </span>

        <el-input-number
          v-model="state.numerisch.soll[name]"
          :step="1"
          @change="setNumerisch(name)"
        />

      </div>

    </el-card>


    <br>


    <!-- NUMERISCHE IST -->
    <el-card>

      <template #header>
        Numerische Istwerte
      </template>

      <div v-for="(value, name) in state.numerisch.ist" :key="name">

        <span style="width:150px; display:inline-block">
          {{ name }}
        </span>

        <el-tag type="info">
          {{ value }}
        </el-tag>

      </div>

    </el-card>


    <br>


    <!-- BINAER SOLL -->
    <el-card>

      <template #header>
        Binäre Sollwerte
      </template>

      <div v-for="(value, name) in state.binaer.soll" :key="name">

        <span style="width:150px; display:inline-block">
          {{ name }}
        </span>

        <el-switch
          v-model="state.binaer.soll[name]"
          @change="setBinaer(name)"
        />

      </div>

    </el-card>


    <br>


    <!-- BINAER IST -->
    <el-card>

      <template #header>
        Binäre Istwerte
      </template>

      <div v-for="(value, name) in state.binaer.ist" :key="name">

        <span style="width:150px; display:inline-block">
          {{ name }}
        </span>

        <el-tag
          :type="value ? 'success' : 'danger'"
        >
          {{ value ? "TRUE" : "FALSE" }}
        </el-tag>

      </div>

    </el-card>


  </div>

</template>


<script setup>

import { reactive } from "vue"


const state = reactive({

  numerisch:
  {
    soll: {},
    ist: {}
  },

  binaer:
  {
    soll: {},
    ist: {}
  }

})


// STATE LADEN

async function loadState()
{

  const res = await fetch("http://localhost:8000/state")

  const data = await res.json()

  state.numerisch = data.numerisch
  state.binaer = data.binaer

}


// NUMERISCH SETZEN

async function setNumerisch(name)
{

  await fetch(
    `http://localhost:8000/numerisch/soll/${name}`,
    {
      method: "POST",

      headers:
      {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        value: state.numerisch.soll[name]
      })
    }
  )

}


// BINAER SETZEN

async function setBinaer(name)
{

  await fetch(
    `http://localhost:8000/binaer/soll/${name}`,
    {
      method: "POST",

      headers:
      {
        "Content-Type": "application/json"
      },

      body: JSON.stringify({
        value: state.binaer.soll[name]
      })
    }
  )

}


// initial laden

loadState()

</script>
