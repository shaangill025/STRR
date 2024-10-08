import { useRouter } from 'vue-router'
export const useBcrosNavigate = () => {
  const config = useRuntimeConfig()
  const account = useBcrosAccount()
  const router = useRouter()

  /** Redirect to the given URL with necessary BCROS args */
  function redirect (url: string) {
    // get account id and set in params
    const redirectURL = new URL(url)
    const accountId = account.currentAccount.id
    if (accountId) {
      redirectURL.searchParams.append('accountid', accountId)
    }
    // assume URL is always reachable
    window.location.assign(redirectURL.href)
  }

  // common redirects
  function goToBcrosHome () { redirect(config.public.registryHomeURL) }
  function goToBcrosLogin (idpHint: string) {
    // using current window location as redirect for now
    // TODO: TC - review this once test deploy for redirects is complete
    window.location.assign(`${config.public.authWebURL}signin/${idpHint}/${window.location.href}`)
  }
  function goToEditProfile () { redirect(config.public.authWebURL + 'userprofile') }
  function goToAccountInfo () {
    redirect(config.public.authWebURL + `account/${account.currentAccount.id}/settings/account-info`)
  }
  function goToTeamMembers () {
    redirect(config.public.authWebURL + `account/${account.currentAccount.id}/settings/team-members`)
  }
  function goToTransactions () {
    redirect(config.public.authWebURL + `account/${account.currentAccount.id}/settings/transactions`)
  }
  function goToCreateSbcAccount () {
    router.push('/finalization')
  }
  function goToCreateAccount () {
    router.push('/create-account')
  }
  function goToSetupAccount () {
    redirect(config.public.authWebURL + 'setup-account')
  }
  function goToTosPage () {
    router.push('/terms-of-service')
  }

  return {
    redirect,
    goToBcrosHome,
    goToBcrosLogin,
    goToAccountInfo,
    goToTosPage,
    goToCreateSbcAccount,
    goToCreateAccount,
    goToEditProfile,
    goToSetupAccount,
    goToTeamMembers,
    goToTransactions
  }
}
