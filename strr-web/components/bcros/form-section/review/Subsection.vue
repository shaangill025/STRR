<template>
  <div class="bg-white py-[22px] px-[30px] mobile:px-[8px]">
    <div class="flex flex-row justify-between w-full desktop:mb-[40px]">
      <div class="flex flex-col w-full">
        <div class="flex flex-row justify-between w-full mb-[24px] mobile:flex-col">
          <BcrosFormSectionReviewItem
            :title="tContact('fullName')"
            :content="getNames()"
          />
          <BcrosFormSectionReviewItem
            :title="tContact('phoneNumber')"
            :content="state.phoneNumber?.toString() ?? '-'"
          />
          <BcrosFormSectionReviewItem
            :title="tContact('emailAddress')"
            :content="state.emailAddress ?? '-'"
          />
        </div>
        <div class="flex flex-row justify-between w-full mobile:flex-col">
          <BcrosFormSectionReviewItem
            :title="tContact('dateOfBirth')"
            :content="getDateOfBirth()"
          />
          <BcrosFormSectionReviewItem
            :title="tContact('faxNumberReview')"
            :content="state?.faxNumber === '' ? '-': state.faxNumber"
          />
          <BcrosFormSectionReviewItem :title="tContact('mailingAddress')">
            <p>{{ state.address }}</p>
            <p v-if="state.addressLineTwo">
              {{ state.addressLineTwo }}
            </p>
            <p>{{ `${state.city ?? '-'} ${state.province ?? '-'} ${state.postalCode ?? '-'}` }}</p>
            <p>{{ `${state.country ? regionNamesInEnglish.of(state.country) : '-'}` }}</p>
          </BcrosFormSectionReviewItem>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

const t = useNuxtApp().$i18n.t
const tContact = (translationKey: string) => t(`create-account.contact-form.${translationKey}`)

const { state, primary } = defineProps<{
  state: ContactInformationI | SecondaryContactInformationI
  primary: boolean
}>()

const { me } = useBcrosAccount()

const getNames = () => {
  const secondaryContactState: SecondaryContactInformationI = state as SecondaryContactInformationI
  const names = {
    first: primary ? me?.profile.firstname : secondaryContactState.firstName,
    middle: primary ? '' : secondaryContactState.middleName,
    last: primary ? me?.profile.lastname : secondaryContactState.lastName
  }
  const nameString = names.first
    ? `${names.first}${names.middle ? ` ${names.middle} ` : ' '}${names.last}`
    : '-'
  return nameString
}

const regionNamesInEnglish = new Intl.DisplayNames(['en'], { type: 'region' })

const getDateOfBirth = () => {
  if (!state.birthDay || !state.birthMonth || !state.birthYear) {
    return '-'
  }
  const date = new Date(`${state.birthMonth} ${state.birthDay} ${state.birthYear}`)
  return date.toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>
