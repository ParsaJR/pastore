<script setup lang="ts">
import { ref } from 'vue'
import type { NavigationMenuItem, SidebarProps } from '@nuxt/ui'

const open = ref(true)

// Ignore the props for the example
defineProps<Pick<SidebarProps, 'variant' | 'side'>>()

const items: NavigationMenuItem[] = [
    {
        label: 'Overview',
        icon: 'i-lucide-house',
        to: "/admin",
        exact: true
    },
    {
        label: 'Pastes',
        icon: 'i-lucide-file-code',
        badge: '4',
        to: "/admin/pastes",
        exact: true
    },
    // {
    //   label: 'Branding',
    //   icon: 'i-lucide-users'
    // }
]
</script>

<template>
    <div class="flex flex-1" :class="[
        variant === 'inset' && 'bg-neutral-50 dark:bg-neutral-950',
        side === 'right' && 'flex-row-reverse'
    ]">
        <USidebar title="Pastore" close v-model:open="open" variant="sidebar" collapsible="icon" side="left" :ui="{
            container: 'h-full'
        }">

            <UNavigationMenu :items="items" orientation="vertical" :ui="{ link: 'p-1.5 overflow-hidden' }" />
        </USidebar>

        <div
            class="flex-1 flex flex-col overflow-hidden lg:peer-data-[variant=floating]:my-4 peer-data-[variant=inset]:m-4 lg:peer-data-[variant=inset]:not-peer-data-[collapsible=offcanvas]:ms-0 peer-data-[variant=inset]:rounded-xl peer-data-[variant=inset]:shadow-sm peer-data-[variant=inset]:ring peer-data-[variant=inset]:ring-default bg-default">
            <div class="h-(--ui-header-height) shrink-0 flex items-center px-4" :class="[
                variant !== 'floating' && 'border-b border-default',
                side === 'right' && 'justify-end'
            ]">
                <UButton icon="i-lucide-panel-left" color="neutral" variant="ghost" aria-label="Toggle sidebar"
                    @click="open = !open" />
            </div>

            <div class="flex-1 p-4 overflow-auto">
                <Suspense>
                    <RouterView></RouterView>
                </Suspense>
            </div>
        </div>
    </div>
</template>
