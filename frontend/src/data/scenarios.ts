/**
 * Synthetic demonstration scenarios for the SCANNAI prototype.
 * Carefully crafted to demonstrate both high-risk procedural fallacies
 * and legitimate communications (false-positive prevention).
 *
 * NOTE: These scenarios are submitted directly to the real backend.
 * No scores or outcomes are hardcoded here.
 */

export interface DemoScenario {
  id: string;
  title: string;
  subtitle: string;
  category: 'EXTORTION' | 'OFFICIAL' | 'BANKING' | 'COMMERCIAL';
  threatSummary: string;
  messageText: string;
}

export const DEMO_SCENARIOS: DemoScenario[] = [
  {
    id: 'digital-arrest',
    title: 'Digital Arrest Scam',
    subtitle: 'Coercive video confinement & fake warrant',
    category: 'EXTORTION',
    threatSummary: 'Impersonates Cyber Crime Branch, demands immediate Skype video confinement, enforces coercive secrecy.',
    messageText:
      'URGENT: This is Cyber Crime Branch New Delhi. You are placed under DIGITAL ARREST immediately on Skype video call. A non-bailable arrest warrant has been issued in your name. Do not disconnect the video camera or inform your family or lawyer until asset verification is complete.',
  },
  {
    id: 'legitimate-ecourts',
    title: 'Legitimate e-Courts Notice',
    subtitle: 'Authentic judicial hearing notice with CNR',
    category: 'OFFICIAL',
    threatSummary: 'Official judicial summons with verified CNR number, official gov.in portal, and explicit no-fee warning.',
    messageText:
      'e-Courts Services: Case CNR DLCT010012342024 listed for hearing on 15-11-2024 before Court Room 302, Tis Hazari Courts, Delhi. Official summons copy available on https://services.ecourts.gov.in. No court fees are collected via phone calls or unverified links.',
  },
  {
    id: 'fraudulent-upi-clearance',
    title: 'Fraudulent UPI Clearance',
    subtitle: 'Bogus RBI asset verification escrow',
    category: 'BANKING',
    threatSummary: 'Claims bank account flagged in money laundering, orders urgent transfer to a bogus RBI clearance UPI handle.',
    messageText:
      'RBI Compliance Notice: Your bank account has been flagged for suspicious high-value money laundering activity. As per court clearance procedure, you must immediately transfer a mandatory verification clearance deposit of Rs 48,500 to the official verification clearance account via UPI: rbi.investigation.officer@okhdfcbank to prevent immediate asset seizure under PMLA.',
  },
  {
    id: 'legitimate-commercial-upi',
    title: 'Legitimate Commercial Order',
    subtitle: 'Everyday e-commerce delivery notice',
    category: 'COMMERCIAL',
    threatSummary: 'Standard retail invoice notification with optional UPI pay-on-delivery. Zero urgency or legal threat.',
    messageText:
      'Your monthly grocery order from FreshMart has been confirmed. Total amount payable: Rs 1,450. You may complete your payment at delivery using UPI handle: freshmart.retail@okhdfcbank or through cash. Thank you for shopping with FreshMart.',
  },
  {
    id: 'customs-ncb-extortion',
    title: 'Customs / NCB Extortion',
    subtitle: 'FedEx parcel drug seizure demand',
    category: 'EXTORTION',
    threatSummary: 'Alleges contraband seized in an international courier parcel, threatens immediate NCB arrest unless penalty is paid.',
    messageText:
      'FedEx International Courier Alert: A parcel sent under your name from Mumbai to Singapore containing contraband and illegal narcotics was seized at Mumbai International Airport Customs. Narcotics Control Bureau (NCB) has initiated legal prosecution. Contact our customs clearance agent immediately to pay customs penalty to avoid criminal detention.',
  },
];
