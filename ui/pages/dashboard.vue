<template>
    <div class="flex flex-col items-center h-screen w-full gap-5">
        <h1 class="text-2xl lg:text-3xl font-bold text-center text-black p-4 rounded-md mb-10">Archive Scraper Bot</h1>

        <Form></Form>
        
        <!-- Placing the log inside a collapsible -->
        <UCollapsible class="flex flex-col gap-2 lg:w-5xl w-full" v-model:open="open">
            <UButton
            label="Show Logs"
            color="neutral"
            variant="subtle"
            trailing-icon="i-lucide-chevron-down"
            block
            />

            <template #content>
                <Log></Log>
            </template>
        </UCollapsible>

    </div>
</template>

<script lang="ts" setup>
const open = ref(false)
</script>