Imports System.Windows.forms

Class MainWindow

    Dim cDialog As New ColorDialog()

    Dim a_seg_col As System.Drawing.Color
    Dim b_seg_col As System.Drawing.Color
    Dim c_seg_col As System.Drawing.Color
    Dim d_seg_col As System.Drawing.Color
    Dim e_seg_col As System.Drawing.Color
    Dim f_seg_col As System.Drawing.Color
    Dim g_seg_col As System.Drawing.Color
    Dim dp_seg_col As System.Drawing.Color

    Private Sub seg_disp_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles a_seg_disp.MouseDown, b_seg_disp.MouseDown, c_seg_disp.MouseDown, d_seg_disp.MouseDown, e_seg_disp.MouseDown, f_seg_disp.MouseDown, g_seg_disp.MouseDown, dp_seg_disp.MouseDown

        If (cDialog.ShowDialog() = Forms.DialogResult.OK) Then
            Dim temp_color As System.Drawing.Color = cDialog.Color ' update with user selected color.

            If sender Is a_seg_disp Then
                a_seg_col = temp_color
            End If
            If sender Is b_seg_disp Then
                b_seg_col = temp_color
            End If
            If sender Is c_seg_disp Then
                c_seg_col = temp_color
            End If
            If sender Is d_seg_disp Then
                d_seg_col = temp_color
            End If
            If sender Is e_seg_disp Then
                e_seg_col = temp_color
            End If
            If sender Is f_seg_disp Then
                f_seg_col = temp_color
            End If
            If sender Is g_seg_disp Then
                g_seg_col = temp_color
            End If
            If sender Is dp_seg_disp Then
                dp_seg_col = temp_color
            End If

            sender.Fill = New SolidColorBrush(Color.FromRgb(Math.Min((temp_color.R / 2) + 128.0, 255), Math.Min((temp_color.G / 2.0) + 128.0, 255), Math.Min((temp_color.B / 2.0) + 128.0, 255)))

        End If

        update()
    End Sub

    Sub update()

        Dim codestring As String = "["

        codestring += "[0x" & a_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & a_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & a_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & b_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & b_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & b_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & c_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & c_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & c_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & d_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & d_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & d_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & e_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & e_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & e_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & f_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & f_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & f_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & g_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & g_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & g_seg_col.B.ToString("X2") & "], "

        codestring += "[0x" & dp_seg_col.R.ToString("X2") & ", "
        codestring += "0x" & dp_seg_col.G.ToString("X2") & ", "
        codestring += "0x" & dp_seg_col.B.ToString("X2") & "]"

        codestring += "]"


        TextBox1.Text = codestring
    End Sub
End Class
