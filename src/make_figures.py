from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Paths:
    root: Path

    @property
    def figs_dir(self) -> Path:
        return self.root / "archive" / "latex" / "figures"


def binary_entropy_bits(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))


def ensure_matplotlib():
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # noqa: F401
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "matplotlib is required to generate figures. "
            "Install it in your environment and re-run."
        ) from exc


def save_pdf(fig, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")


def fig1_credit_ledger(paths: Paths) -> None:
    ensure_matplotlib()
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyArrowPatch, Rectangle

    fig, ax = plt.subplots(figsize=(12.0, 4.0))
    ax.set_axis_off()

    # Boxes - now with TWO resource boxes (state credit + protocol optimization)
    box_style = dict(linewidth=1.5)

    # State credit reservoir (depleting resource)
    state_credit = Rectangle((0.01, 0.52), 0.22, 0.38, fill=False, **box_style)
    # Protocol knowledge (non-depleting)
    protocol = Rectangle((0.01, 0.10), 0.22, 0.38, fill=False, **box_style, linestyle="--")
    # Code register
    register = Rectangle((0.38, 0.25), 0.22, 0.50, fill=False, **box_style)
    # Heat bath
    bath = Rectangle((0.74, 0.25), 0.22, 0.50, fill=False, **box_style)

    for patch in (state_credit, protocol, register, bath):
        ax.add_patch(patch)

    # Labels
    ax.text(
        0.12,
        0.76,
        "State Credit\n(bias + correlations)",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
    )
    ax.text(
        0.12,
        0.58,
        "conserved resource\n(depletes)",
        ha="center",
        va="center",
        fontsize=8,
        color="#555",
    )

    ax.text(
        0.12,
        0.34,
        "Protocol Optimization\n(geometry)",
        ha="center",
        va="center",
        fontsize=9.5,
        fontweight="bold",
    )
    ax.text(
        0.12,
        0.16,
        "reduces waste\n(does not deplete)",
        ha="center",
        va="center",
        fontsize=8,
        color="#555",
    )

    ax.text(0.49, 0.50, "Code Register\n(write/erase)", ha="center", va="center", fontsize=10)
    ax.text(0.85, 0.50, "Heat Bath\nat $T$", ha="center", va="center", fontsize=10)

    # Arrows
    def arrow(x0, y0, x1, y1, text: str, y_text: float, x_text: float = None):
        ax.add_patch(
            FancyArrowPatch(
                (x0, y0),
                (x1, y1),
                arrowstyle="->",
                mutation_scale=12,
                linewidth=1.5,
                color="black",
            )
        )
        if x_text is None:
            x_text = (x0 + x1) / 2
        ax.text(x_text, y_text, text, ha="center", va="center", fontsize=8.5)

    # State credit -> Register (reduces W_rev)
    arrow(0.23, 0.71, 0.38, 0.60, "spend credit\n(reduces $W_{rev}$)", 0.82, 0.305)

    # Protocol -> Register (reduces W_irr)
    arrow(0.23, 0.29, 0.38, 0.40, "efficient path\n(reduces $W_{irr}$)", 0.47, 0.305)

    # Register -> Bath
    arrow(0.60, 0.50, 0.74, 0.50, "entropy\nexport", 0.62)
    arrow(0.49, 0.25, 0.85, 0.25, "dissipate heat ($Q$)", 0.12)

    ax.text(
        0.50,
        0.01,
        "State credit is conserved (spending requires prior accumulation). Protocol efficiency is not conserved (always available if implementable).",
        ha="center",
        va="bottom",
        fontsize=8.5,
    )

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)

    save_pdf(fig, paths.figs_dir / "fig1_credit_ledger.pdf")
    plt.close(fig)


def fig2_tilted_register(paths: Paths) -> None:
    ensure_matplotlib()
    import matplotlib.pyplot as plt

    p = np.linspace(0, 1, 501)
    H = binary_entropy_bits(p)
    negentropy = 1 - H

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(p, H, label=r"$W_{\min}/(k_BT\ln 2)=H(p)$", linewidth=2)
    ax.plot(p, negentropy, label=r"negentropy $=1-H(p)$", linewidth=2)

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel(r"bias $p=P(X=1)$")
    ax.set_ylabel("bits")
    ax.set_title("Tilted Register: Erasure Cost vs. Stored Credit")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)

    save_pdf(fig, paths.figs_dir / "fig2_tilted_register.pdf")
    plt.close(fig)


def fig3_side_information(paths: Paths) -> None:
    ensure_matplotlib()
    import matplotlib.pyplot as plt

    # Binary symmetric channel: Y predicts X with error rate e.
    e = np.linspace(0.0, 0.5, 501)
    Hb = binary_entropy_bits(e)  # H_b(e)
    I = 1 - Hb  # For uniform X: I(X;Y)=1-H_b(e)
    W_erase = Hb  # H(X|Y)=H_b(e)
    W_out_max = I  # in units of kBT ln2 (extractable work)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(I, W_erase, label=r"erasure bound: $W_{\min}/(k_BT\ln 2)=H(X|Y)$", linewidth=2)
    ax.plot(
        I,
        W_out_max,
        label=r"max extraction: $W_{\max}^{\mathrm{out}}/(k_BT\ln 2)=I(X;Y)$",
        linewidth=2,
    )

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.02, 1.02)
    ax.set_xlabel(r"mutual information $I(X;Y)$ (bits)")
    ax.set_ylabel(r"work in units of $k_BT\ln 2$")
    ax.set_title("Correlation Credit: Erasure vs. Work Extraction")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)

    save_pdf(fig, paths.figs_dir / "fig3_side_information.pdf")
    plt.close(fig)


def fig4_thermodynamic_length(paths: Paths) -> None:
    """
    Illustrate thermodynamic length / Fisher geometry on univariate Gaussians.

    Fisher metric for (mu, sigma) is: ds^2 = (dmu^2 + 2 dsigma^2) / sigma^2.
    With y = sqrt(2)*sigma, this is 2 * (dx^2 + dy^2) / y^2 (Poincaré half-plane up to scale).
    """

    ensure_matplotlib()
    import matplotlib.pyplot as plt

    # Choose two Gaussian endpoints.
    # Pick an example where an axis-aligned protocol is visibly longer than the geodesic:
    # when sigma is small, horizontal motion in mu is expensive under the Fisher metric.
    mu0, sigma0 = 0.0, 0.2
    mu1, sigma1 = 6.0, 1.0

    x0, y0 = mu0, np.sqrt(2.0) * sigma0
    x1, y1 = mu1, np.sqrt(2.0) * sigma1

    # Geodesic in Poincaré half-plane: circle orthogonal to boundary y=0 (or vertical line).
    if np.isclose(x0, x1):
        x_geo = np.full(300, x0)
        y_geo = np.linspace(y0, y1, 300)
    else:
        xc = (x1 * x1 + y1 * y1 - x0 * x0 - y0 * y0) / (2.0 * (x1 - x0))
        R = np.sqrt((x0 - xc) ** 2 + y0**2)

        t0 = np.arctan2(y0, x0 - xc)
        t1 = np.arctan2(y1, x1 - xc)
        ts = np.linspace(t0, t1, 400)
        x_geo = xc + R * np.cos(ts)
        y_geo = R * np.sin(ts)

    # Distances (thermodynamic lengths) in the scaled metric ds^2 = 2*(dx^2+dy^2)/y^2.
    # Poincaré half-plane distance:
    d_poincare = np.arccosh(1.0 + ((x0 - x1) ** 2 + (y0 - y1) ** 2) / (2.0 * y0 * y1))
    L_geo = np.sqrt(2.0) * d_poincare

    # Axis-aligned path length: horizontal at y0, then vertical at x1.
    L_axis = np.sqrt(2.0) * (abs(x1 - x0) / y0 + abs(np.log(y1 / y0)))

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(x_geo, y_geo, label="Fisher geodesic", linewidth=2)
    ax.plot([x0, x1, x1], [y0, y0, y1], label="axis-aligned protocol", linewidth=2)

    ax.scatter([x0, x1], [y0, y1], s=45, zorder=3)
    ax.text(x0, y0 + 0.08, "A", ha="center", va="bottom", fontsize=11)
    ax.text(x1, y1 + 0.08, "B", ha="center", va="bottom", fontsize=11)

    ax.set_xlabel(r"mean $\mu$")
    ax.set_ylabel(r"$\sqrt{2}\,\sigma$")
    ax.set_title("Thermodynamic Length in Fisher Geometry (Univariate Gaussians)")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, loc="upper right")

    text = "\n".join(
        [
            r"lengths in Fisher metric:",
            rf"$L_{{geo}}\approx {L_geo:.2f}$",
            rf"$L_{{axis}}\approx {L_axis:.2f}$",
            rf"ratio $\approx {L_axis/L_geo:.2f}\times$",
        ]
    )
    ax.text(
        0.02,
        0.02,
        text,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, linewidth=0.0),
    )

    save_pdf(fig, paths.figs_dir / "fig4_thermodynamic_length.pdf")
    plt.close(fig)


def fig5_dimensional_aliasing(paths: Paths) -> None:
    """
    Toy illustration: "bits depend on embedding dimension".

    Two clusters in D dimensions are separated only along the first k_sep dimensions.
    As projection dimension k increases, distinguishability increases until k captures
    the separating dimensions, then plateaus.
    """

    ensure_matplotlib()
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(42)

    n_points = 250
    D_full = 20
    k_sep = 5
    delta_per_dim = 1.0
    sigma = 1.2

    center_A = np.zeros(D_full)
    center_B = np.zeros(D_full)
    center_B[:k_sep] = delta_per_dim

    cluster_A = center_A + sigma * rng.standard_normal((n_points, D_full))
    cluster_B = center_B + sigma * rng.standard_normal((n_points, D_full))

    all_points = np.vstack([cluster_A, cluster_B])
    labels = np.array([0] * n_points + [1] * n_points)

    # Distinguishability curve: Mahalanobis distance d' under identity covariance (||delta|| / sigma).
    delta = center_B - center_A
    ks = np.arange(1, D_full + 1)
    dprime = np.sqrt(np.cumsum(delta**2)) / sigma

    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6), gridspec_kw={"width_ratios": [1.15, 1.0, 1.0]})

    # Left: d' vs k.
    ax = axes[0]
    ax.plot(ks, dprime, "o-", linewidth=2, markersize=4, color="#2563eb")
    ax.axvline(k_sep, color="#dc2626", linestyle=":", alpha=0.8, label=f"separating dims ($k={k_sep}$)")
    ax.set_xlabel("projection dimension $k$")
    ax.set_ylabel(r"distinguishability ($d'$)")
    ax.set_title("Distinguishability vs. $k$")
    ax.set_xlim(1, 12)
    ax.set_ylim(0, float(dprime[k_sep - 1]) * 1.15)
    ax.legend(fontsize=8, loc="lower right", frameon=False)
    ax.grid(True, alpha=0.3)

    # Middle: k=1 projection (jittered).
    ax = axes[1]
    proj_1d = all_points[:, 0]
    y_jitter = 0.12 * rng.standard_normal(len(proj_1d))
    ax.scatter(proj_1d[labels == 0], y_jitter[labels == 0], alpha=0.55, s=18, c="#3b82f6", label="Class A")
    ax.scatter(proj_1d[labels == 1], y_jitter[labels == 1], alpha=0.55, s=18, c="#f97316", label="Class B")
    ax.set_xlabel(r"projection ($k=1$)")
    ax.set_yticks([])
    ax.set_title(r"$k=1$: aliasing (overlap)")
    ax.legend(fontsize=8, frameon=False, loc="upper right")
    ax.grid(True, alpha=0.3, axis="x")

    # Right: k=5 subspace shown in 2D via PCA.
    ax = axes[2]
    proj_k = all_points[:, :k_sep]
    proj_kc = proj_k - proj_k.mean(axis=0, keepdims=True)
    _, _, Vt = np.linalg.svd(proj_kc, full_matrices=False)
    Z = proj_kc @ Vt.T[:, :2]
    ax.scatter(Z[labels == 0, 0], Z[labels == 0, 1], alpha=0.55, s=18, c="#3b82f6", label="Class A")
    ax.scatter(Z[labels == 1, 0], Z[labels == 1, 1], alpha=0.55, s=18, c="#f97316", label="Class B")
    ax.set_xlabel(r"PC1 (subspace $k=5$)")
    ax.set_ylabel("PC2")
    ax.set_title(r"$k=5$: separation")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, frameon=False, loc="upper right")

    fig.tight_layout()
    save_pdf(fig, paths.figs_dir / "fig5_dimensional_aliasing.pdf")
    plt.close(fig)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = Paths(root=root)

    fig1_credit_ledger(paths)
    fig2_tilted_register(paths)
    fig3_side_information(paths)
    fig4_thermodynamic_length(paths)
    fig5_dimensional_aliasing(paths)
    print(f"Wrote figures to: {paths.figs_dir}")


if __name__ == "__main__":
    main()
