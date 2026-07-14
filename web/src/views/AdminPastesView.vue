<script setup lang="ts">
import { h, ref, resolveComponent, useTemplateRef, watch } from 'vue'
import { getCoreRowModel, getPaginationRowModel, useVueTable } from '@tanstack/vue-table'
import type { TableColumn } from '@nuxt/ui'
import { useAPI } from '@/composables/api'
import type { PasteSchema } from '@/types/ApiTypes'
import { useLanguageDetector, useShikiHighlighter } from '@/composables/language-detect'

const UButton = resolveComponent('UButton')


const content = ref("")
const content_modal = ref("")

const data = ref(await useAPI().getAllPastes(1, 10))

 watch(() => content.value, async () => {
     const lang = useLanguageDetector(content.value)
     content_modal.value = await useShikiHighlighter(content.value, lang)
     }
     // Execute the watcher's callback immediately once, on the first creation of the component.
 , {immediate: true})


const content_modal_show = ref(false)

type Payment = {
    id: string
    date: string
    email: string
    amount: number
}

const columns: TableColumn<PasteSchema>[] = [
    {
        accessorKey: 'id',
        header: '#ID',
        cell: ({ row }) => `#${row.getValue('id')}`
    },
    {
        accessorKey: 'shortcode',
        header: "Shortcode"
    },
    {
        accessorKey: 'created_at',
        header: 'Created At',
        cell: ({ row }) => {
            return new Date(row.getValue('created_at')).toLocaleString('en-US', {
                day: 'numeric',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            })
        }
    },
    {
        accessorKey: 'is_one_time',
        header: 'One time?',
        cell: ({ row }) => {
            const yes = row.getValue("is_one_time")
            if (yes) return "Yes"
            else return "No"
        }
    },
    {
        accessorKey: 'expires_at',
        header: 'Expires At',
        cell: ({ row }) => {
            return new Date(row.getValue('expires_at')).toLocaleString('en-US', {
                day: 'numeric',
                month: 'short',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false
            })
        }
    },
    {
        accessorKey: 'view_count',
        header: 'view_count',
        meta: {
            class: {
                th: 'text-right',
                td: 'text-right font-medium'
            }
        },
    },
    {
        header: "Operations",
        cell: ({row}) => {
            return h(UButton, {
                color: 'primary',
                veriant: 'subtle',
                icon: 'lucide:file-code-corner',
                label: 'Content',
                onClick: () => {
                    content.value = row.original.content
                    content_modal_show.value = true
                }
            })
        }
    },
]

const pagination = ref({
  pageIndex: 0,
  pageSize: 10
})


watch(
  pagination,
  async () => {
    console.log("page changed", pagination.value)
    data.value = await useAPI().getAllPastes(
      pagination.value.pageIndex + 1,
      pagination.value.pageSize
    )
  },
  { deep: true }
)
const globalFilter = ref('')

</script>

<template>
    <div class="w-full space-y-4 pb-4">
        <div class="flex px-4 py-3.5 border-b border-accented">
            <UInput v-model="globalFilter" class="max-w-sm" placeholder="Filter..." />
        </div>

        <UTable v-model:global-filter="globalFilter" v-model:pagination="pagination"
            :pagination-options="{ manualPagination: true, rowCount: data.total_items, pageCount: data.total_pages}"
            :data="data.items" :columns="columns" class="flex-1" />

        <UModal fullscreen title="Content" v-model:open="content_modal_show">
            <template #body>
                <div class="m-4" v-html="content_modal">
                </div>
            </template>
        </UModal>
        <div class="flex justify-end border-t border-default pt-4 px-4">
            <UPagination :page="pagination.pageIndex + 1" :items-per-page="pagination.pageSize"
                :total="data.total_items" @update:page="page => pagination.pageIndex = page - 1" />
        </div>
    </div>

</template>
