<script setup lang="ts">
import { useAPI } from '@/composables/api'
import { useToast } from '@/composables/toast'
import type { APIError } from '@/types/ApiTypes'
import type { FormSubmitEvent, AuthFormField } from '@nuxt/ui'
import { sensitiveHeaders } from 'http2'
import * as v from 'valibot'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'


const router = useRouter()

// There is any browser that doesn't have/support localstorage? Let's use this 
function LocalStorageAvailable() {
	let storage;
	try {
		storage = window["localStorage"];
		const x = "__storage_test__";
		storage.setItem(x, x);
		storage.removeItem(x);
		return true;
	} catch (e) {
		return (
			e instanceof DOMException &&
			e.name === "QuotaExceededError" &&
			// acknowledge QuotaExceededError only if there's something already stored
			storage &&
			storage.length !== 0
		);
	}
}

const schema = v.object({
	username: v.pipe(v.string()),
	password: v.pipe(v.string(), v.minLength(6, 'Must be at least 6 characters'), v.nonEmpty())
})


type Schema = v.InferOutput<typeof schema>

const fields = ref<AuthFormField[]>([{
	name: 'username',
	type: 'text',
	label: 'Email',
	placeholder: 'Enter your username',
	required: true,
	defaultValue: '',
}, {
	name: 'password',
	label: 'Password',
	type: 'password',
	placeholder: 'Enter your password',
	required: true,
	defaultValue: '',
},
])

async function onSubmit(payload: FormSubmitEvent<Schema>) {
	const data = new URLSearchParams({
		username: payload.data.username,
		password: payload.data.password,
	})

	let ok = true
	try {
		const token = await useAPI().getToken(data)
		if (!LocalStorageAvailable()) {
			useToast("Sorry. Your browser doesn't have a sane localStorage.", 'error')
			return
		}
		localStorage.setItem("token", token.access_token);
		useToast("Welcome.", 'success')
	}
	catch (error) {
		ok = false
		const err = error as APIError
		useToast(`${err.statusText}`,'error')
	}
	if (ok) {
		router.push("admin")
	}
}
</script>

<template>
	<div class="h-full flex flex-col items-center justify-center gap-4 p-4">
		<UPageCard class="w-full max-w-md">
			<UAuthForm title="Login" :schema="schema" description="Enter your credentials" icon="i-lucide-user"
				:fields="fields" @submit="onSubmit" />
		</UPageCard>
	</div>
</template>
