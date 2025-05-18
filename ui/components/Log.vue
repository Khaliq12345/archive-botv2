<template>
  <div class="lg:p-5 lg:w-5xl w-full">
    <UContainer>
      <!-- Main Logs Card-->
      <div class="mx-auto px-4 py-5 my-3 text-center">
        <h1 class="text-2xl font-bold mb-4">View Logs</h1>

        <!-- Input -->
        <UInput 
            color="neutral" v-model="logOf" type="text" icon="i-heroicons-link" 
            class="w-full [&_input]:text-black [&_input]:dark:text-black"
            placeholder="Show Logs of :" 
        />
        <UButton class="text-black" :disabled="!logOf" :loading="loading" @click="getLogs" 
            label="Process" color="primary" icon="i-heroicons-clipboard-document" size="xl"
        />
        
        <!-- Outputs -->
        <div class="bg-info-100 rounded-xl border-1 mx-auto px-4 pt-5 my-4">
          <div v-if="loading" class="my-5 mx-5 h-110 flex justify-center items-center">
            <UProgress />
          </div>
          <div v-else class="">
            <p class="text-start font-bold">Log File of : {{ logOf2 }}</p>
            <USeparator class="my-4" />
            <UTextarea :rows="20" :autoresize="false" v-model="logGot" 
                class="w-full mb-4 input textarea whitespace-pre font-mono" placeholder="Nothing to show ..." 
            />
          </div>
        </div>

        <!-- Refresh -->
        <div class="justify-start flex">
          <UButton label="Refresh Logs" :disabled="logGot.length==0" icon="i-heroicons-arrow-path"
            class="justify-center text-blue-500" @click="getLogs" color="info"/>
            <!-- Clear -->
            <UButton label="Clear Logs" :disabled="logOf2.length==0" icon="i-heroicons-archive-box-x-mark"
            class="justify-center ml-5 text-red-500" @click="clearLogs" color="error" />
        </div>

      </div>
    </UContainer>
  </div>
</template>

<script setup lang="ts">

// Variables
const logOf = ref("");
const logOf2 = ref("");
const logGot = ref("");
const loading = ref(false);

// clear all logs
const clearLogs = async () => {
  loading.value = true
  try {
    const response = await $fetch('/api/clear-log', {
      method: 'GET',
      params: {
        'key': logOf2.value
      }
    }) as any
    console.log("status : ", response)

    await getLogs()

  } catch (error) {
    console.error('Erreur de requete:', error);
  } finally {
    loading.value = false
  }
}

// refresh logs
const getLogs = async () => {
  loading.value = true
  try {
    const response = await $fetch('/api/get-log', {
      method: 'GET',
      params: {
        'key': logOf.value
      },
    }) as any
    console.log("status : ", response)

    logGot.value = response

    logOf2.value = logOf.value

  } catch (error) {
    console.error('Erreur de requete:', error);
  } finally {
    loading.value = false
  }
}
</script>



<style scoped>
.container {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
    0 10px 10px rgba(0, 0, 0, 0.22);
  position: relative;
  overflow: hidden;
  max-width: 100%;
  min-height: 480px;
}

.input {
  -webkit-text-fill-color: black;
  border-color: black;
}

/* .textarea {
  overflow-x: scroll; 
} */
</style>