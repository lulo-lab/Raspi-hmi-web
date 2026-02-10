
<template>
  <div>
    <h2>Registeransicht</h2>

    <el-button
      type="primary"
      @click="aktualisieren"
      style="margin-bottom: 20px"
    >
      Aktualisieren
    </el-button>

    <el-table
      :data="registers"
      border
      style="width: 100%"
      height="600"
    >

      <el-table-column
        prop="index"
        label="Index"
        width="70"
      />

      <el-table-column
        label="Sollwert"
        width="140"
      >
        <template #default="scope">
          <el-input-number
            v-model="scope.row.sollwert"
            :min="0"
            :max="65535"
            :disabled="!scope.row.freigabe"
            style="width: 120px"
          />
        </template>
      </el-table-column>

      <el-table-column
        prop="istwert"
        label="Istwert"
        width="100"
      />

      <el-table-column
        label="Freigabe"
        width="90"
      >
        <template #default="scope">
          <el-checkbox v-model="scope.row.freigabe"/>
        </template>
      </el-table-column>

    </el-table>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const registers = ref([]);


/*
Initialisierung (nur einmal)
*/
const initRegisters = async () => {

  try {

    const res = await fetch("http://localhost:8000/register");

    if (!res.ok)
      throw new Error("Register konnten nicht geladen werden");

    const data = await res.json();

    registers.value = data.register.map((value, index) => ({
      index,
      sollwert: value,
      istwert: value,
      freigabe: false
    }));

  }
  catch (err) {

    console.error(err);

  }

};


/*
Istwerte lesen
*/
const readIstwerte = async () => {

  try {

    const res = await fetch("http://localhost:8000/register");

    if (!res.ok)
      throw new Error("Register konnten nicht gelesen werden");

    const data = await res.json();

    data.register.forEach((value, index) => {

      registers.value[index].istwert = value;

    });

  }
  catch (err) {

    console.error(err);

  }

};


/*
Freigegebene Sollwerte schreiben
*/
const writeFreigegebene = async () => {

  try {

    for (const reg of registers.value) {

      if (!reg.freigabe)
        continue;

      const res = await fetch(
        `http://localhost:8000/register/${reg.index}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            value: reg.sollwert
          })
        }
      );

      if (!res.ok)
        throw new Error(`Fehler bei Register ${reg.index}`);

    }

  }
  catch (err) {

    console.error(err);

  }

};


/*
Aktualisieren Button
*/
const aktualisieren = async () => {

  await writeFreigegebene();

  await readIstwerte();

};


/*
Startup
*/
onMounted(async () => {

  await initRegisters();

  await readIstwerte();

});

</script>

