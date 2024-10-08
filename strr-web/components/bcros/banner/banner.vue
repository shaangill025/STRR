<template>
  <div
    data-test-id="banner"
    :class="`
        flex justify-center bg-white absolute w-full top-0 left-0 min-h-[104px] shadow-md
        py-[30px] px-[70px]
        m:flex-col m:min-h-[116px] m:px-[8px]
        ${hideButtons ? 'm:min-h-[70px]' : ''}
      `"
  >
    <div class="flex justify-between px-4 w-full max-w-[1360px]">
      <slot />
      <div v-if="!hideButtons">
        <div class="mobile:hidden">
          <BcrosButtonsPrimary
            v-if="applicationId"
            :label="tBanner('approve')"
            :action="() => applicationId && approveApplication(applicationId)"
            variant="outline"
            class-name="ml-[16px]"
          />
          <BcrosButtonsPrimary
            v-if="applicationId"
            :label="tBanner('reject')"
            :action="() => applicationId && rejectApplication(applicationId)"
            variant="outline"
            class-name="ml-[16px]"
          />
          <BcrosButtonsPrimary
            v-if="registrationId"
            :label="tBanner('issue')"
            :action="() => registrationId && issueCertificate(registrationId)"
            variant="outline"
            class-name="ml-[16px]"
          />
        </div>
        <div class="desktop:hidden flex">
          <a
            v-if="applicationId"
            class="mr-[16px] py-[10px]"
            :on-click="() => applicationId && approveApplication(applicationId)"
          >
            {{ tBanner('approve') }}
          </a>
          <a
            v-if="applicationId"
            class="mr-[16px] py-[10px]"
            :on-click="() => applicationId && rejectApplication(applicationId)"
          >
            {{ tBanner('reject') }}
          </a>
          <a
            v-if="registrationId"
            class="mr-[16px] py-[10px]"
            :on-click="() => registrationId && issueCertificate(registrationId)"
          >
            {{ tBanner('issue') }}
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { hideButtons = true } = defineProps<{
  hideButtons?: boolean
  applicationId?: string
  registrationId?: string
}>()
const { t } = useTranslation()
const tBanner = (text: string) => t(`banner.${text}`)
const { issueCertificate } = useRegistrations()
const { approveApplication, rejectApplication } = useApplications()
</script>
