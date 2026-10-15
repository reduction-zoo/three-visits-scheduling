module

public import Mathlib.Computability.TuringMachine.Computable

@[expose] public section

namespace ThreeVisitsScheduling

/-- Q001's self-delimiting binary natural; length is logarithmic, not unary. -/
def encodeNat (n : Nat) : List Bool :=
  let bits := (Nat.toDigits 2 n).map (fun c => c == '1')
  List.replicate bits.length true ++ [false] ++ bits

def encodeList {α : Type} (encode : α → List Bool) (xs : List α) : List Bool :=
  encodeNat xs.length ++ xs.flatMap encode

def encodeOption {α : Type} (encode : α → List Bool) : Option α → List Bool
  | none => [false]
  | some x => true :: encode x

/-- None denotes mathematical nonexistence, never an execution error. -/
def searchOutput {I W : Type} (legal : I → Bool) (witness : I → W → Bool)
    (x : I) : Option W → Prop
  | some w => legal x = true ∧ witness x w = true
  | none => legal x = true ∧ ¬ ∃ w, witness x w = true


def legalSource (x : List Nat) : Bool := x.all (fun d => d > 0)
def legalTarget := legalSource
def visits (deadlines : List Nat) (k : Nat) (word : List Nat) : Bool :=
  word.length == deadlines.length*k && word.all (fun v => v < deadlines.length) &&
  (List.range deadlines.length).all (fun v =>
    let positions := (word.zipIdx.filter (fun (task,_) => task == v)).map (fun (_,i) => i+1)
    positions.length == k &&
    ((0 :: positions).zip positions).all (fun (a,b) => b-a ≤ deadlines[v]?.getD 0))
def encodeSource := encodeList encodeNat
def encodeTarget := encodeSource
def validSourceOutput := searchOutput legalSource (fun x => visits x 2)
def validTargetOutput := searchOutput legalTarget (fun x => visits x 3)

/-- Both algorithms use Q001's explicit bit encoding and TM2 cost model.
Recovery receives the full pair of source instance and target output. -/
def Reduction (forward : (List Nat) → (List Nat))
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)) : Prop :=
  Nonempty (Turing.TM2ComputableInPolyTime encodeSource encodeTarget forward) ∧
  Nonempty (Turing.TM2ComputableInPolyTime
    (fun input => encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2)
    (encodeOption (encodeList encodeNat)) recover) ∧
  (∃ bound : Polynomial Nat, ∀ x,
    (encodeTarget (forward x)).length ≤ bound.eval (encodeSource x).length) ∧
  (∃ bound : Polynomial Nat, ∀ input,
    ((encodeOption (encodeList encodeNat)) (recover input)).length ≤
      bound.eval (encodeSource input.1 ++ (encodeOption (encodeList encodeNat)) input.2).length) ∧
  (∀ x, legalSource x = true → legalTarget (forward x) = true) ∧
  (∀ x, legalSource x = true → ∀ y, validTargetOutput (forward x) y →
    validSourceOutput x (recover (x, y)))

def Goal : Prop :=
  ∃ (forward : (List Nat) → (List Nat))
    (recover : (List Nat) × Option (List Nat) → Option (List Nat)), Reduction forward recover

/-- Open question only; this placeholder is not a solution. -/
theorem solve : Goal := by
  sorry

end ThreeVisitsScheduling
