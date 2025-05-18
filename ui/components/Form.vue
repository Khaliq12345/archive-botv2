<template>
    <div class="bg-gray-200 lg:w-5xl w-full p-5 rounded-lg">
      <form class="space-y-6">
        <div>
          <label class="block text-base text-gray-800 mb-1">Base Url</label>
          <input type="text" v-model="baseUrl" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div>
          <label class="block text-base text-gray-800 mb-1">HTML Content</label>
          <textarea type="text" rows="5" v-model="htmlContent" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div>
          <label class="block text-base text-gray-800 mb-1">Primary Keywords</label>
          <input type="text" v-model="primaryKeywords" placeholder="seperate multiple by ';'" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div>
          <label class="block text-base text-gray-800 mb-1">Secondary Keywords</label>
          <input type="text" v-model="secondaryKeywords" placeholder="seperate multiple by ';'" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div class="flex justify-center">
          <button
            @click="startProcess"
            type="button" class="bg-[#4ba3e3] text-white px-6 py-2 rounded hover:bg-[#368acc] transition cursor-pointer"
          >
            START BOT
          </button>
        </div>
      </form>
      
      <!-- // Show alert -->
      <UAlert
        title="Bot started"
        color="success"
        class="w-full"
        v-show="showAlert"
        close
        @click="showAlert = !showAlert"
      />
    </div>
</template>


<script setup lang="ts">
const baseUrl = ref('')
const htmlContent = ref('')
const primaryKeywords = ref('')
const secondaryKeywords = ref('')
const showAlert = ref(false)

async function startProcess() {
  // seperating the keywords before sending them
  const pks = primaryKeywords.value.split(';')
  const sks = secondaryKeywords.value.split(';')
  if (baseUrl.value && htmlContent.value) {
    await $fetch('/api/start-process', {
      method: 'post',
      params: {
        base_url: baseUrl.value
      },
      body: {
        'html': htmlContent.value,
        'primary_keywords': pks,
        'secondary_keywords': sks
      }
    })

    showAlert.value = !showAlert.value
  }
}
</script>


<style>

</style>