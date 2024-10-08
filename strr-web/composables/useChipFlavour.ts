export const useChipFlavour = () => {
  const { t } = useTranslation()
  const tRegistryDashboardStatus = (translationKey: string) => t(`registryDashboard.statusChip.${translationKey}`)

  const getChipFlavour = (status: string): StatusChipFlavoursI['flavour'] => {
    switch (status) {
      case 'ACTIVE':
        return {
          text: tRegistryDashboardStatus('active'),
          alert: AlertsFlavourE.SUCCESS
        }
      case 'DENIED':
        return {
          text: tRegistryDashboardStatus('denied'),
          alert: AlertsFlavourE.ALERT
        }
      case 'APPROVED':
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: tRegistryDashboardStatus('approved')
        }
      case 'ISSUED':
        return {
          alert: AlertsFlavourE.SUCCESS,
          text: tRegistryDashboardStatus('issued')
        }
      case 'REJECTED':
        return {
          alert: AlertsFlavourE.ALERT,
          text: tRegistryDashboardStatus('rejected')
        }
      case 'PENDING':
        return {
          alert: AlertsFlavourE.WARNING,
          text: tRegistryDashboardStatus('pending')
        }
      case 'UNDER_REVIEW':
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('underReview')
        }
      case 'SUBMITTED':
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('submitted')
        }
      case 'PAID':
        return {
          alert: AlertsFlavourE.APPLIED,
          text: tRegistryDashboardStatus('paid')
        }
      default:
        return {
          alert: AlertsFlavourE.MESSAGE,
          text: ''
        }
    }
  }

  return { getChipFlavour }
}
