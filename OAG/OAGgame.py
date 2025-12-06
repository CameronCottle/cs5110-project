from player import Owner, Adversary, OwnerAction, AdversaryAction

class OAGGame:
    def __init__(self, owner: Owner, adversary: Adversary):
        self.owner = owner
        self.adversary = adversary

    def payoff(self, owner_action: OwnerAction, adv_action: AdversaryAction):
        U  = self.owner.U
        P  = self.owner.P
        C_p = self.owner.C_p
        gamma = self.owner.gamma

        G  = self.adversary.G
        C_a = self.adversary.C_a

        # Protect | Attack
        if owner_action == OwnerAction.PROTECT and adv_action == AdversaryAction.ATTACK:
            return (U - C_p - gamma * P,gamma * G - C_a)

        # Protect | Abstain
        if owner_action == OwnerAction.PROTECT and adv_action == AdversaryAction.ABSTAIN:
            return (U - C_p,0)

        # Defect | Attack
        if owner_action == OwnerAction.DEFECT and adv_action == AdversaryAction.ATTACK:
            return (U - P,G - C_a)

        # Defect | Abstain
        if owner_action == OwnerAction.DEFECT and adv_action == AdversaryAction.ABSTAIN:
            return (U,0)

        print("Invalid action, Don't know how you even got here")

    def all_profiles(self):
        profiles = []
        for o_act in OwnerAction:
            for a_act in AdversaryAction:
                payoff = self.payoff(o_act, a_act)
                profiles.append((o_act, a_act, payoff))
        return profiles

    def best_responses(self):
        profiles = self.all_profiles()

        # Owner best responses
        owner_best = {}
        for a_act in AdversaryAction:
            subset = [p for p in profiles if p[1] == a_act]
            max_owner = max(p[2][0] for p in subset)
            owner_best[a_act] = {p[0] for p in subset if p[2][0] == max_owner}

        # Adversary best responses
        adv_best = {}
        for o_act in OwnerAction:
            subset = [p for p in profiles if p[0] == o_act]
            max_adv = max(p[2][1] for p in subset)
            adv_best[o_act] = {p[1] for p in subset if p[2][1] == max_adv}

        return owner_best, adv_best

    def pure_equilibria(self):
        owner_best, adv_best = self.best_responses()
        equilibria = []

        for o_act in OwnerAction:
            for a_act in AdversaryAction:
                if o_act in owner_best[a_act] and a_act in adv_best[o_act]:
                    equilibria.append((o_act, a_act))

        return equilibria
    
    def mixed_equilibrium(self):
        a, e = self.payoff(OwnerAction.PROTECT, AdversaryAction.ATTACK)
        b, _ = self.payoff(OwnerAction.PROTECT, AdversaryAction.ABSTAIN)
        c, g = self.payoff(OwnerAction.DEFECT, AdversaryAction.ATTACK)
        d, _ = self.payoff(OwnerAction.DEFECT, AdversaryAction.ABSTAIN)

        denom_q = (a - b - c + d)
        denom_p = (g - e)

        if abs(denom_q) < 1e-8 or abs(denom_p) < 1e-8:
            return None
        
        # probability of attack & protect
        q = (d - b) / denom_q 
        p = g / denom_p

        return {
            "Probability Owner Protects": p,
            "Probability Owner Defects": 1 - p,
            "Probability Adversary Attacks": q,
            "Probability Adversary Abstains": 1 - q
        }
