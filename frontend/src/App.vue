<template>

  <el-tabs v-model="activeTab">

    <el-tab-pane label="Steuerung" name="control">

      <ControlPanel />

    </el-tab-pane>


    <el-tab-pane label="Register" name="register">

      <RegisterView />

    </el-tab-pane>

  </el-tabs>

</template>


<script setup>

import { ref } from "vue"

import ControlPanel from "./components/ControlPanel.vue"
import RegisterView from "./components/RegisterView.vue"

const activeTab = ref("control")

</script>
