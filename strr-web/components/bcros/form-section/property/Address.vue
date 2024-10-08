<template>
  <div data-test-id="form-section-address">
    <BcrosFormSection :title="t('createAccount.propertyForm.rentalUnitAddress')">
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup
          name="nickname"
          class="d:pr-[16px] flex-grow"
          :help="t('createAccount.propertyForm.nicknameHelp')"
        >
          <UInput v-model="nickname" aria-label="nickname" :placeholder="t('createAccount.propertyForm.nickname')" />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="country" class="d:pr-[16px] flex-grow">
          <USelect
            v-model="country"
            :options="countryItems"
            option-attribute="name"
            class="w-full"
            aria-label="country"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup name="Address" class="d:pr-[16px] flex-grow">
          <UInput
            :id="id"
            v-model="address"
            :placeholder="t('createAccount.contactForm.address')"
            aria-label="address"
            @input="onAddressInput"
            @click="addressComplete()"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:mb-[16px]">
        <UFormGroup
          name="AddressLineTwo"
          class="d:pr-[16px] flex-grow"
          :error="fieldErrors.addressLineTwo"
        >
          <UInput
            v-model="addressLineTwo"
            aria-label="address line two"
            :placeholder="t('createAccount.contactForm.addressLineTwo')"
          />
        </UFormGroup>
      </div>
      <div class="flex flex-row justify-between w-full mb-[40px] mobile:flex-col mobile:mb-[16px]">
        <UFormGroup
          name="city"
          class="d:pr-[16px] flex-grow mobile:mb-[16px]"
          :error="fieldErrors.city"
        >
          <UInput v-model="city" aria-label="city" :placeholder="t('createAccount.contactForm.city')" />
        </UFormGroup>
        <UFormGroup
          name="province"
          class="d:pr-[16px] flex-grow mobile:mb-[16px]"
          :error="addressNotInBC ? 'Address must be in BC' :''"
        >
          <UInput
            v-model="province"
            aria-label="province"
            :placeholder="t('createAccount.contactForm.province')"
            disabled
          />
        </UFormGroup>
        <UFormGroup
          name="postalCode"
          class="d:pr-[16px] flex-grow mobile:mb-[16px]"
          :error="fieldErrors.postalCode"
        >
          <UInput
            v-model="postalCode"
            aria-label="postal code"
            :placeholder="t('createAccount.contactForm.postalCode')"
          />
        </UFormGroup>
      </div>
    </BcrosFormSection>
  </div>
</template>

<script setup lang="ts">
import { CountryItem } from '@/interfaces/address-i'
import countries from '@/utils/countries.json'
const { t } = useTranslation()

const country = defineModel<string>('country')
const address = defineModel<string>('address')
const addressLineTwo = defineModel<string>('addressLineTwo')
const city = defineModel<string>('city')
const province = defineModel<string>('province')
const postalCode = defineModel<string>('postalCode')
const nickname = defineModel<string>('nickname')
const countryItems = ref<CountryItem[]>([])
const fieldErrors = ref({
  addressLineTwo: '',
  city: '',
  postalCode: ''
})

const addressComplete = () => {
  if (typeof country.value === 'string') {
    enableAddressComplete(id, 'CA', false)
  }
}

const resetFieldError = (field: keyof typeof fieldErrors.value) => {
  fieldErrors.value[field] = ''
}

const onAddressInput = () => {
  addressLineTwo.value = ''
  city.value = ''
  postalCode.value = ''
  resetFieldError('addressLineTwo')
  resetFieldError('city')
  resetFieldError('postalCode')
  addressComplete()
}

const {
  id,
  defaultCountryIso2,
  enableAddressComplete,
  addressNotInBC
} = defineProps<{
  id: string,
  defaultCountryIso2: string,
  enableAddressComplete:(id: string, countryIso2: string, countrySelect: boolean) => void,
  addressNotInBC?: boolean
}>()

country.value = defaultCountryIso2

// Rental addresses for registration can only be in Canada
onMounted(() => {
  countryItems.value = countries
    .filter(country => country.iso2 === 'CA')
    .map(country => ({
      value: country.iso2,
      name: country.en
    }))
})

</script>
