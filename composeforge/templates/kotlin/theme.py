"""
composeforge.templates.kotlin.theme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Material 3 theme templates: Color.kt, Type.kt, Theme.kt.
"""


def kt_color(pkg: str) -> str:
    """Génère Color.kt avec la palette Material 3."""
    return f"""\
package {pkg}

import androidx.compose.ui.graphics.Color

// ── Primary ─────────────────────────────
val Primary            = Color(0xFF6650A4)
val OnPrimary          = Color(0xFFFFFFFF)
val PrimaryContainer   = Color(0xFFEADDFF)
val OnPrimaryContainer = Color(0xFF21005D)

// ── Secondary ───────────────────────────
val Secondary            = Color(0xFF625B71)
val OnSecondary          = Color(0xFFFFFFFF)
val SecondaryContainer   = Color(0xFFE8DEF8)
val OnSecondaryContainer = Color(0xFF1D192B)

// ── Tertiary ────────────────────────────
val Tertiary            = Color(0xFF7D5260)
val OnTertiary          = Color(0xFFFFFFFF)
val TertiaryContainer   = Color(0xFFFFD8E4)
val OnTertiaryContainer = Color(0xFF31111D)

// ── Surface / Background ─────────────────
val Background   = Color(0xFFFFFBFE)
val OnBackground = Color(0xFF1C1B1F)
val SurfaceColor = Color(0xFFFFFBFE)
val OnSurface    = Color(0xFF1C1B1F)

// ── Error ────────────────────────────────
val Error   = Color(0xFFB3261E)
val OnError = Color(0xFFFFFFFF)

// ── Dark variants ─────────────────────────
val PrimaryDark    = Color(0xFFD0BCFF)
val OnPrimaryDark  = Color(0xFF381E72)
val BackgroundDark = Color(0xFF1C1B1F)
val OnBgDark       = Color(0xFFE6E1E5)
val SurfaceDark    = Color(0xFF1C1B1F)
val OnSurfaceDark  = Color(0xFFE6E1E5)
"""


def kt_type(pkg: str) -> str:
    """Génère Type.kt avec la typographie Material 3."""
    return f"""\
package {pkg}

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val AppTypography = Typography(
    displayLarge = TextStyle(
        fontFamily   = FontFamily.Default,
        fontWeight   = FontWeight.Normal,
        fontSize     = 57.sp,
        lineHeight   = 64.sp,
        letterSpacing = (-0.25).sp
    ),
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.SemiBold,
        fontSize   = 32.sp,
        lineHeight = 40.sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.SemiBold,
        fontSize   = 28.sp,
        lineHeight = 36.sp
    ),
    titleLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Bold,
        fontSize   = 22.sp,
        lineHeight = 28.sp
    ),
    bodyLarge = TextStyle(
        fontFamily    = FontFamily.Default,
        fontWeight    = FontWeight.Normal,
        fontSize      = 16.sp,
        lineHeight    = 24.sp,
        letterSpacing = 0.5.sp
    ),
    bodyMedium = TextStyle(
        fontFamily    = FontFamily.Default,
        fontWeight    = FontWeight.Normal,
        fontSize      = 14.sp,
        lineHeight    = 20.sp,
        letterSpacing = 0.25.sp
    ),
    labelSmall = TextStyle(
        fontFamily    = FontFamily.Default,
        fontWeight    = FontWeight.Medium,
        fontSize      = 11.sp,
        lineHeight    = 16.sp,
        letterSpacing = 0.5.sp
    )
)
"""


def kt_theme(pkg: str, app_name: str) -> str:
    """Génère Theme.kt avec Material 3 dynamic color."""
    return f"""\
package {pkg}

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext

private val LightColors = lightColorScheme(
    primary            = Primary,
    onPrimary          = OnPrimary,
    primaryContainer   = PrimaryContainer,
    onPrimaryContainer = OnPrimaryContainer,
    secondary            = Secondary,
    onSecondary          = OnSecondary,
    secondaryContainer   = SecondaryContainer,
    onSecondaryContainer = OnSecondaryContainer,
    tertiary            = Tertiary,
    onTertiary          = OnTertiary,
    tertiaryContainer   = TertiaryContainer,
    onTertiaryContainer = OnTertiaryContainer,
    background   = Background,
    onBackground = OnBackground,
    surface      = SurfaceColor,
    onSurface    = OnSurface,
    error   = Error,
    onError = OnError,
)

private val DarkColors = darkColorScheme(
    primary      = PrimaryDark,
    onPrimary    = OnPrimaryDark,
    background   = BackgroundDark,
    onBackground = OnBgDark,
    surface      = SurfaceDark,
    onSurface    = OnSurfaceDark,
)

@Composable
fun AppTheme(
    darkTheme    : Boolean = isSystemInDarkTheme(),
    dynamicColor : Boolean = true,
    content      : @Composable () -> Unit
) {{
    val colorScheme = when {{
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {{
            val ctx = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(ctx) else dynamicLightColorScheme(ctx)
        }}
        darkTheme -> DarkColors
        else      -> LightColors
    }}

    MaterialTheme(
        colorScheme = colorScheme,
        typography  = AppTypography,
        content     = content
    )
}}
"""
