
library(dplyr)
library(MASS)

sim_eq_data <- function(
    n, mu_y, mu_x, sigma_xe,
    gamma_y, gamma_x, alpha_x = NULL,
    eps_tnsfmrs = NULL, xi_tnsfmrs = NULL
) {
    #   Parameters for structural equations
    n_y <- length(mu_y)
    mu_y <- matrix(mu_y, ncol = 1)
    eps_tnsfmrs <- if (is.null(eps_tnsfmrs)) {
        rep(list(NULL), n_y)
    } else {
        eps_tnsfmrs
    }
    #   Parameters for covariate generation
    n_x <- length(mu_x)
    mu_x <- matrix(mu_x, ncol = 1)
    xi_tnsfmrs <- if (is.null(xi_tnsfmrs)) {
        rep(list(NULL), n_x)
    } else {
        xi_tnsfmrs
    }
    #   Parameters for dummy indicators generation
    alpha_x <- if (is.null(alpha_x)) {
        rep(list(NULL), n_x)
    } else {
        alpha_x
    }
    #   Jointly generate covariate and dependent variable errors
    xi_eps <- mvrnorm(n, rep(0, n_x + n_y), sigma_xe)
    #   Construct covariates first
    xi <- matrix(xi_eps[, 1:n_x], ncol = n_x)
    xi <- mapply(
        function(f, a) if (is.null(f)) a else f(a),
        xi_tnsfmrs,
        t(xi)
    )
    xi <- matrix(xi, ncol = n_x, byrow = TRUE)
    x <- sweep(t(xi), 1, mu_x, FUN = "+")
    x <- mapply(
        function(a, x) if (is.null(a)) x else 1 * (x < a),
        alpha_x,
        x
    )
    x <- matrix(x, ncol = n_x, byrow = TRUE)
    #   Construct dependent variables second
    eps <- matrix(xi_eps[, (n_x + 1):(n_x + n_y)], ncol = n_y)
    eps <- mapply(
        function(f, a) if (is.null(f)) a else f(a),
        eps_tnsfmrs,
        t(eps)
    )
    eps <- matrix(eps, ncol = n_y, byrow = TRUE)
    y <- x %*% gamma_x + eps
    y <- sweep(t(y), 1, mu_y, FUN = "+")
    y <- solve(diag(n_y) - gamma_y, y)
    #   Save data
    rownames(y) <- paste("y", 1:n_y, sep = "")
    colnames(x) <- paste("x", 1:n_x, sep = "")
    colnames(eps) <- paste("eps", 1:n_y, sep = "")
    colnames(xi) <- paste("xi", 1:n_x, sep = "")
    y <- cbind(t(y), x, eps, xi)
    y <- as_tibble(y)
    return(y)
}
