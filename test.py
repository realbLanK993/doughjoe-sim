import random
import math
from dataclasses import dataclass
from typing import List

CAPACITY = 150
WINDOW = 120

@dataclass
class Booking:
    size: int
    price_per_pax: float
    channel: str
    days_out: int
    cancel_prob: float
    noshow_prob: float

class HardModeGame:
    def __init__(self):
        self.capacity = CAPACITY
        self.window = WINDOW
        self.accepted: List[Booking] = []
        self.rejected_count = 0
        self.base_demand = self._generate_demand_profile()
        self.price_pressure = 1.0

    def _generate_demand_profile(self):
        profile = {
            'leisure_peak': random.randint(70, 100),
            'business_peak': random.randint(10, 40),
            'demand_shock': random.random() < 0.3
        }
        if profile['demand_shock']:
            profile['shock_type'] = random.choice(['family_surge', 'business_drought'])
            profile['shock_start'] = random.randint(20, 80)
        return profile

    def _get_lambda(self, days_out: int) -> float:
        base = 0
        if days_out > 60:
            base = 1.0 + (120 - days_out) * 0.01
        elif days_out > 30:
            base = 1.8
        else:
            base = 3.0 + (30 - days_out) * 0.1

        if (self.base_demand.get('demand_shock') and 
            self.base_demand.get('shock_start', 0) - 10 <= days_out <= self.base_demand.get('shock_start', 0) + 10):
            if self.base_demand.get('shock_type') == 'family_surge':
                base *= 1.8
            elif self.base_demand.get('shock_type') == 'business_drought':
                base *= 0.4

        return base * 1.5

    def _adjust_price_pressure(self):
        if self.rejected_count > 15 and self.price_pressure > 0.7:
            self.price_pressure = max(0.7, self.price_pressure - 0.05)

    def generate_booking(self, days_out: int) -> Booking:
        lam = self._get_lambda(days_out)
        if random.random() > lam / (lam + 1):
            return None

        # CHANNEL — FIXED: ' bod' → 'Direct'
        if days_out > 60:
            channel = random.choices(['OTA', 'Direct', 'Corp'], [0.75, 0.20, 0.05])[0]
        elif days_out > 30:
            channel = random.choices(['OTA', 'Direct', 'Corp'], [0.50, 0.35, 0.15])[0]
        else:
            channel = random.choices(['OTA', 'Direct', 'Corp'], [0.20, 0.30, 0.50])[0]

        # Size
        size = 1 if channel == 'Corp' and random.random() < 0.94 else self._truncated_nb()

        # Price with pressure
        base_mu = {'OTA': 5.3, 'Direct': 5.7, 'Corp': 6.2}[channel]
        mu = base_mu + (self.price_pressure - 1.0) * 2
        mu += (120 - days_out) * 0.006
        sigma = 0.5
        price = math.exp(random.gauss(mu, sigma))
        price = round(price * self.price_pressure, 2)

        # Risk — FIXED: ' c' → 'Corp'
        cancel_p = {'OTA': 0.15, 'Direct': 0.10, 'Corp': 0.05}[channel]
        noshow_p = {'OTA': 0.10, 'Direct': 0.08, 'Corp': 0.05}[channel]
        if size >= 5:
            cancel_p += 0.05
            noshow_p += 0.05

        return Booking(size, price, channel, days_out, cancel_p, noshow_p)

    def _truncated_nb(self) -> int:
        while True:
            val = sum(1 for _ in range(1) if random.random() < 0.55) + 1
            if val >= 1:
                return val

    def play(self):
        print(f"\n{'='*60}")
        print(f"FLIGHT RM: HARD MODE | {self.capacity} SEATS | {self.window} DAYS")
        print(f"Market is unpredictable. No hints. No target.")
        print(f"{'='*60}")
        input("Press Enter to begin...")

        current_day = self.window
        booking_count = 0

        while current_day > 0:
            booking = self.generate_booking(current_day)
            if booking is None:
                current_day -= 1
                continue

            booking_count += 1
            risk = "LOW" if booking.cancel_prob + booking.noshow_prob < 0.15 else \
                   "MED" if booking.cancel_prob + booking.noshow_prob < 0.25 else "HIGH"

            print(f"\n--- Booking #{booking_count} | {current_day} days out ---")
            print(f"Size: {booking.size} | Price/pax: ${booking.price_per_pax:.0f} | Channel: {booking.channel}")
            print(f"Total: ${booking.price_per_pax * booking.size:.0f} | Risk: {risk}")

            choice = input("Accept? (Y/N): ").strip().upper()
            if choice == 'Y':
                self.accepted.append(booking)
                print(f"  Accepted. Booked: {sum(b.size for b in self.accepted)}")
            else:
                self.rejected_count += 1
                self._adjust_price_pressure()
                print("  Rejected.")

            current_day -= 1

        # Final
        print(f"\n{'-'*50}")
        print("DEPARTURE! Simulating show-ups...")
        show_ups = sum(
            sum(1 for _ in range(b.size) if random.random() > b.cancel_prob + b.noshow_prob)
            for b in self.accepted
        )
        revenue = sum(
            b.price_per_pax * sum(1 for _ in range(b.size) if random.random() > b.cancel_prob + b.noshow_prob)
            for b in self.accepted
        )
        bumps = max(0, show_ups - self.capacity)
        penalty = bumps * 2000
        net = revenue - penalty

        print(f"\nFINAL RESULT")
        print(f"Show-ups: {show_ups} | Bumps: {bumps} | Penalty: ${penalty:,}")
        print(f"NET REVENUE: ${net:,.0f}")

        if net > 38000:
            print("ELITE: Top 1%")
        elif net > 32000:
            print("Strong")
        elif net > 28000:
            print("Average")
        else:
            print("Market crushed you.")

        print(f"\nHIDDEN MARKET TRUTH:")
        print(f"  Business peak: {self.base_demand['business_peak']} days out")
        print(f"  Demand shock: {self.base_demand.get('shock_type', 'None')}")

        again = input("\nPlay again? (Y/N): ").upper()
        if again == 'Y':
            HardModeGame().play()

if __name__ == "__main__":
    HardModeGame().play()
